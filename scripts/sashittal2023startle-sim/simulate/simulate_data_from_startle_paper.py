"""
This python script simulates data based on the Startle paper, here: 
    https://doi.org/10.1101/2022.12.18.520935

and the Cassiopeia documentation, here:
    https://cassiopeia-lineage.readthedocs.io/en/latest/index.html

We also vary the casette length, as this parameter was not specified in the 
Startle paper. We assume it was length 1 but this value was set to length 3 and
10 in Chan et al and McKenna et al, respectively.
See https://cassiopeia-lineage.readthedocs.io/en/latest/api/reference/cassiopeia.sim.Cas9LineageTracingDataSimulator.html

NOTE to EKM: To run on cluster, do:
    module load Python3/3.10.4
    pip3.10 install typing_extensions --user
    pip3.10 install git+https://github.com/YosefLab/Cassiopeia@master#egg=cassiopeia-lineage --user 

Contact: EKM
"""
import argparse
import cassiopeia.sim as cassim
import numpy
import os
import pandas
import treeswift
import sys


def castree_to_treeswift(castree):
    # Make copy of tree using treeswift
    newick = castree.get_newick()
    tstree = treeswift.read_tree_newick(newick)
    
    for node in tstree.traverse_postorder():
        if node.is_root():
            node.set_edge_length(0.0)
            node.muts = []
        else:
            if node.is_leaf():
                node.id = node.label
            nid = node.id

            # Set node ID of parent
            pid = castree.parent(nid)
            parent = node.get_parent()
            parent.id = pid  

            # Set mutations on incoming edge
            node.muts = castree.get_mutations_along_edge(pid, nid,
                            treat_missing_as_mutations=False)

            # Set length on incoming edge
            elen = castree.get_branch_length(pid, nid)
            node.set_edge_length(elen)

    # Re-root tree by adding fake node
    root = tstree.root

    if root.id != '0':
        sys.exit("Root does not have ID 0!\n")
    
    if len(root.child_nodes()) != 1:
        sys.exit("Root does not have outdegree 1!\n")

    new_node = treeswift.Node(edge_length=0.0, label=root.id)
    new_node.id = root.id  # Root is now represented as a leaf
    new_node.muts = []

    root.add_child(new_node)
    root.id = "FAKE"

    return tstree


def write_model_tree(tstree, output):
    # Re-label tree to save mutations and internal node id's
    for node in tstree.traverse_postorder():
        tmp = [str("(c%d,%d)" % x) for x in node.muts]
        node.label = "[NODE=" + node.id + ",MUTS=[" + ','.join(tmp) + "]]"

    # Write tree to file
    with open(output, 'w') as fo:
        fo.write(tstree.newick() + '\n')

    # Re-label tree again
    for node in tstree.traverse_postorder():
        if node.is_leaf():
            node.label = node.id
        else:
            node.label = None


def estimate_mutation_priors(lt_sim, castree):
    cmat = castree.character_matrix
    nstate = lt_sim.number_of_states

    count_edited_states_all = 0
    count_edited_states = {}
    for state in range(1, nstate+1):
        # Dirchlet counts to avoid states with zero probability
        count_edited_states[state] = 1
        count_edited_states_all += 1

    [nrow, ncol] = cmat.shape
    for i in range(nrow):
        for j in range(ncol):
            val = cmat.iat[i,j]
            if val == -1:
                pass
            elif val == 0:
                pass
            else:
                count_edited_states_all += 1
                count_edited_states[val] += 1

    for state in range(1, nstate+1):
        count_edited_states[state] /= count_edited_states_all

    return count_edited_states


def write_mutation_prior(castree, priors, output):
    cmat = castree.character_matrix
    states = sorted(priors.keys())

    with open(output, 'w') as fo:
        fo.write("character,state,probability\n")
        for char in cmat.columns:
            for state in states:
                fo.write("c%s,%d,%1.12f\n" % (char, state, priors[state]))


def write_homoplasy(tree, output):
    mutcounts = {}

    for node in tree.traverse_postorder():
        for mut in node.muts:
            [char, state] = mut

            try:
                x = mutcounts[char]
            except KeyError:
                mutcounts[char] = {}

            try:
                x = mutcounts[char][state]
            except KeyError:
                x = 0

            mutcounts[char][state] = x + 1

    with open(output, 'w') as fo:
        #fo.write("char,state,nmuts,homoplasy\n")

        num_homoplasy_events = 0
        num_homoplasy_chars = 0

        chars = sorted(mutcounts.keys())
        for char in chars:
            homoplasy_char = 0

            for state in mutcounts[char].keys():
                nmuts = mutcounts[char][state]
                homoplasy_event = 0
                if nmuts > 1:
                    homoplasy_event = 1
                    homoplasy_char = 1
                    num_homoplasy_events += 1

                #fo.write("%d,%d,%d,%d\n" % (char, state, nmuts, homoplasy_event))

            if homoplasy_char:
                num_homoplasy_chars += 1

        msg = str("Simulation had %d homoplasy events across %d characters.\n" \
                    % (num_homoplasy_events, num_homoplasy_chars))
        sys.stdout.write(msg)
        fo.write(msg)


def add_c_to_column_names(casmat):
    colmap = {}
    for col in casmat.columns.values.tolist():
        colmap[col] = 'c' + str(col)
    casmat.rename(columns=colmap, inplace=True)


def remove_c_from_column_names(casmat):
    colmap = {}
    for col in casmat.columns.values.tolist():
        colmap[col] = col.replace('c', '')
    casmat.rename(columns=colmap, inplace=True)


def write_character_matrix(casmat, output):
    add_c_to_column_names(casmat)  # Done in Startle paper

    # Create df for root
    cols = list(casmat.columns)
    row = {}
    for key in cols:
        row[key] = 0
    rows = [row]
    root = pandas.DataFrame(rows, columns=cols)

    # Create df with root and characters
    df = pandas.concat([root, casmat])
    df.to_csv(output, sep=',', header=True, index=True)

    remove_c_from_column_names(casmat)


def write_data(lt_sim, castree, outdir):
    # Convert from castree to treeswift
    tstree = castree_to_treeswift(castree)
    casmat = castree.character_matrix

    # Write model tree with mutations and edge lengths
    output = outdir + "/true_tree.nwk"
    write_model_tree(tstree, output)

    # Write model mutation prior
    output = outdir + "/true_mutation_prior.csv"
    priors = lt_sim.mutation_priors
    write_mutation_prior(castree, priors, output)

    # Write estimated mutation prior
    output = outdir + "/estimated_mutation_prior.csv"
    priors = estimate_mutation_priors(lt_sim, castree)
    write_mutation_prior(castree, priors, output)

    # Analyze homoplasy
    output = outdir + "/homoplasy_true.csv"
    write_homoplasy(tstree, output)

    # Write character matrix
    output = outdir + "/character_matrix.csv"
    write_character_matrix(casmat, output)


def simulate_tree_bd(num_lineages, seed):
    startle_initial_birth_scale = 0.5  # From Startle paper; Same as Cassiopeia example
    startle_fitness_base = 1.3         # From Startle paper; Same as Cassiopeia example

    # From Startle paper, the birth and death waiting times were drawn from an
    # exponential distribution (details not specified). We use the same numbers
    # as the Cassiopeia example but we shift the death waiting distribution by
    # one because otherwise all lineages die for some replicates.

    bd_sim = cassim.BirthDeathFitnessSimulator(
                num_extant=num_lineages,
                initial_birth_scale=startle_initial_birth_scale,
                birth_waiting_distribution=lambda scale: numpy.random.exponential(scale),
                death_waiting_distribution=lambda: numpy.random.exponential(1.5) + 1.0,      # Similar to Cassiopeia example
                fitness_base=startle_fitness_base,
                fitness_distribution=lambda: numpy.random.normal(0, 0.5),                    # From Cassiopeia example
                mutation_distribution=lambda: 1.0 if numpy.random.uniform() < 0.5 else 0.0,  # From Cassiopeia example
                random_seed=seed
                )
    model_tree = bd_sim.simulate_tree()
    return model_tree


def simulate_characters_cas(model_tree, num_cassettes, casette_size,
                            mutation_rate, dropout, seed):
    startle_number_of_states = 25  # From Startle paper

    # From Startle paper, the mutation priors were drawn from an exponential
    # distribution. Their example data on Github uses the same distribution.
    numpy.random.seed(seed)
    exp_vals = numpy.random.exponential(size=startle_number_of_states)
    norm_exp_vals = exp_vals / numpy.sum(exp_vals)
    our_priors = {}
    for i in range(0, startle_number_of_states):
        our_priors[i+1] = norm_exp_vals[i]

    print(mutation_rate)

    lt_sim = cassim.Cas9LineageTracingDataSimulator(
                number_of_cassettes=num_cassettes,
                size_of_cassette=casette_size,
                mutation_rate=mutation_rate,
                number_of_states=startle_number_of_states,
                state_generating_distribution=None,
                state_priors=our_priors,
                heritable_silencing_rate=0.0,  # Not in Startle paper
                stochastic_silencing_rate=dropout,
                heritable_missing_data_state=-1,
                stochastic_missing_data_state=-1,
                random_seed=seed
                )
    lt_sim.overlay_data(model_tree)

    return lt_sim


def main(args):
    # Step 1 - Create output directories
    if args.outdir != ".":
        if not os.path.isdir(args.outdir):
            sys.exit("Output directory %s does not exist!" % args.outdir)
    
    # Create first directory if it does not exist
    outdir1 = args.outdir + "/" \
                + "nlin_" + str(args.num_lineages) \
                + "-ncas_" + str(args.num_cassettes) \
                + "-clen_" + str(args.casette_size) \
                + "-mutp_" + str(args.prob_mut) \
                + "-dout_" + str(args.dropout)

    outdir2 = outdir1 + "/" + args.seed

    if os.path.isdir(outdir1):
        if os.path.isdir(outdir2):
            sys.exit("Looks like simulation was already conducted; exiting to avoid overwriting files!")
    else:
        os.mkdir(outdir1)
    os.mkdir(outdir2)

    # Step 1 - Simulate tree
    seed = int(args.seed)  # Convert to int to remove zero padding
    model_tree = simulate_tree_bd(args.num_lineages,
                                  seed)

    # Step 2 - Simulate character matrix down tree
    lt_sim = simulate_characters_cas(model_tree,
                                     args.num_cassettes,
                                     args.casette_size,
                                     args.prob_mut,
                                     args.dropout,
                                     seed)

    # Step 3 - Write data
    write_data(lt_sim, model_tree, outdir2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("-n", "--num_lineages", type=int, default=50,
                        help="Number of extant lineages (cells)")

    parser.add_argument("-m", "--num_cassettes", type=int, default=10,
                        help="Number of cassettes (target sites)")

    parser.add_argument("-p", "--prob_mut", type=float, default=0.1,
                        help="Probability of mutation")

    parser.add_argument("-l", "--casette_size", type=int, default=1,
                        help="Size of cassette")

    parser.add_argument("-d", "--dropout", type=float, default=0.0,
                        help="Probability of allelic dropout")

    parser.add_argument("-s", "--seed", type=str, default="1",
                        help="Integer seed for random number generator")

    parser.add_argument("-o", "--outdir", type=str, default=".",
                        help="Output directory")

    main(parser.parse_args())

