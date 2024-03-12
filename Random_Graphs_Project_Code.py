import networkx


def initialize_test_for_case(case, num_of_n, p):
    # First, we initialize all of our soon-to-be calculated variables.
    num_of_valid_simplicity = 0
    L1 = 0
    L2 = 0
    L3 = 0
    average_size_and_complexity = [[0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0], [0, 0]]

    # Then, we create a Random Graph and perform our test on it, we do that 50 times for every different number of Vertices.
    for i in range(50):
        # Here we create our random graph using the "networkx" library. It is not a directed graph.
        random_graph = networkx.fast_gnp_random_graph(num_of_n, p, seed=None, directed=False)

        # We initialize three lists, to find the top 3 biggest connected components.
        # The lvalue is for the number of nodes it holds,
        # The rvalue is for the index of the first node (in the BFS algorithm).
        biggest_connected_component = [0, -1]
        second_biggest_connected_component = [0, -1]
        third_biggest_connected_component = [0, -1]

        # This will hold all the sizes of connected components that we found.
        sizes_of_connected_components = []

        # List that will hold info about complexity of each calculation.
        connected_components_complexity = []

        # This is an indicator for the maximum complexity that was found.
        complexity_max = 0

        # Here is a flag that marks if we are in a complex calculation or a simple one.
        is_not_complex = True

        # Just like in a BFS search algorithm, we have a list of visited nodes. First it is initialized.
        already_visited = set()

        # For each possible connected component, we iterate through it and check for connectivity.
        for n in range(num_of_n):
            # If we didn't check it, we should do it now.
            if n not in already_visited:
                # We use our BFS helper function to have our set of nodes for a connected component, if it exists.
                connected_component = BFS_Searcher(n, random_graph)

                # Just like in a BFS algorithm, we mark all the visited nodes, to avoid searching them again.
                for node in connected_component:
                    already_visited.add(node)

                # Then, we get our set of edges of the connected component
                graph_edges = list(networkx.edge_bfs(random_graph, n))

                # As given in the articles, this is the calculation for the complexity.
                complexity = 1 + len(graph_edges) - len(connected_component)

                # If we found that our complexity is not simple, we need to treat it according to our case.
                if complexity > 1:
                    # As described in these cases, by the definition of simple and complex complexity
                    if complexity_max > 1 and (case == "Barely Supercritical" or case == "Very Supercritical"):
                        is_not_complex = False

                    # As described in these cases, by the definition of simple and complex complexity
                    if case == "Very Sub-critical" or case == "Barely Sub-critical":
                        is_not_complex = False

                # After finding a connected component, we need to check if he is one of the top 3 biggest connected components.
                if len(connected_component) >= biggest_connected_component[0]:
                    second_biggest_connected_component = biggest_connected_component
                    biggest_connected_component = [len(connected_component), n]

                    # Also we need to update the max value of complexities.
                    complexity_max = complexity

                elif len(connected_component) > second_biggest_connected_component[0]:
                    second_biggest_connected_component = [len(connected_component), n]

                elif len(connected_component) > third_biggest_connected_component[0]:
                    third_biggest_connected_component = [len(connected_component), n]

                connected_components_complexity.append([len(connected_component), complexity])
                sizes_of_connected_components.append(len(connected_component))

        check_if_to_print(case, set(sizes_of_connected_components), str(complexity_max))

        if case == "Critical Window - positive" or case == "Critical Window - negative":
            # We want to find the 10 biggest connected components, so we sort our list.
            sorted_list = sorted(connected_components_complexity, key=lambda x: x[0])

            # And extract the first 10.
            largest_ten_components = sorted_list[-10:]

            # Then, in order to calc the average of the size and complexity, we sum them in their appropriate positions.
            for i in range(10):
                # First place for size of connected component
                average_size_and_complexity[i][0] += largest_ten_components[i][0]

                # Second place is for the complexity of the connected component
                average_size_and_complexity[i][1] += largest_ten_components[i][1]

        # We need to update our Li's.
        L1 += biggest_connected_component[0]
        L2 += second_biggest_connected_component[0]
        L3 += third_biggest_connected_component[0]

        # Now, if we found the that complexity is not complex, we add to the counter.
        if is_not_complex:
            num_of_valid_simplicity += 1

    should_print_averages(case, L1, L2, L3, str(num_of_valid_simplicity), average_size_and_complexity)
    # Add space in the log.
    print()


# This is a helper function that prints results according to the tested case.
def should_print_averages(case, L1, L2, L3, num_of_valid_simplicity, average_size_and_complexity):
    if case == "Critical Window - positive" or case == "Critical Window - negative":
        print("10 largest components (size, complexity): " + str(
            [[x / 50 for x in components_list] for components_list in average_size_and_complexity]))

    else:
        print("**************************************************")
        print("The average size of L1 is: " + str(L1 / 50))
        print()
        print("The average size of L2 is: " + str(L2 / 50))
        print()
        print("The average size of L3 is: " + str(L3 / 50))
        print()
        print("The number of simple graphs found is: " + num_of_valid_simplicity)
        print("**************************************************")


def check_if_to_print(case, to_print_1, to_print_2):
    if case == "Very Sub-critical" or case == "Barely Sub-critical":
        print(to_print_1)
    if case == "Barely Supercritical" or case == "Very Supercritical":
        print("The biggest connected components complexity found is: " + to_print_2)


# Here we search for a connectivity component using "networkx" library.
# We conduct a BFS Search Algorithm on the "graph" variable, starting from node "n1".
# In return, it gives us a connected graph.
# Finally, we return its set of nodes.
def BFS_Searcher(n1, Graph):
    connected_graph = networkx.edge_bfs(Graph, n1)

    # connect_graph is a tuple, so we take only the first of each tuple
    connected_list = [v for u, v in connected_graph]

    # we don't forget to add the first node that was searched
    set_of_n = [n1] + connected_list

    return set(set_of_n)


# Here we create the probability "p" for each test from our explored cases.
# This is used for the "Barely sub-critical" and "Barely supercritical" cases.
def p_for_each_test(plus_or_minus, n, lamda):
    return ((plus_or_minus * lamda) / (n ** (1 / 3)) + 1) / n


###############################################################
#                                                             #
# HERE WE BEGIN TO RUN OUR TESTS FOR EACH CASE, 1-5:          #
#                                                             #
###############################################################

# This is the run that tests Case "Very Sub-critical".
for n in range(10):
    num_of_n = (50000 + 100000 * n)

    # This is the necessary calculation of "p", as required in this case.
    p = 1 / (2 * num_of_n)

    print("*** " + "Very Sub-critical" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(p) + " ***")
    initialize_test_for_case("Very Sub-critical", num_of_n, p)

# This is the run that tests Case "Barely Sub-critical".
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # This is the necessary calculation of "lambda", as required in this case.
    lamda = num_of_n ** 0.01

    # This is the necessary calculation of "p", as required in this case.
    p = p_for_each_test(-1, num_of_n, lamda)

    print("*** " + "Barely Sub-critical" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(p) + " ***")
    initialize_test_for_case("Barely Sub-critical", num_of_n, p)

# This is the run that tests Case "Critical Window" when p = 1/n.
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # Here we calculate the required probability for this test case.
    p = 1 / num_of_n

    print("*** " + "Critical Window - positive" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(
        p) + " ***")
    initialize_test_for_case("Critical Window - positive", num_of_n, p)

# This is the run that tests Case "Critical Window" when p > 1/n
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # Here we calculate the required probability for this test case.
    p = p_for_each_test(1, num_of_n, 2)

    print("*** " + "Critical Window - positive" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(
        p) + " ***")
    initialize_test_for_case("Critical Window - positive", num_of_n, p)

# This is the run that tests Case "Critical Window" when p < 1/n
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # Here we calculate the required probability for this test case.
    p = p_for_each_test(-1, num_of_n, 2)

    print("*** " + "Critical Window - negative" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(
        p) + " ***")
    initialize_test_for_case("Critical Window - negative", num_of_n, p)

# This is the run that tests Case "Barely Supercritical".
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # This is the necessary calculation of "lambda", as required in this case.
    lamda = num_of_n ** 0.01

    # Here we calculate the required probability for this test case.
    p = p_for_each_test(1, num_of_n, lamda)

    print("*** " + "Barely Supercritical" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(p) + " ***")
    initialize_test_for_case("Barely Supercritical", num_of_n, p)

# This is the run that tests Case "Very Supercritical", where p = 2/n.
for n in range(10):
    num_of_n = 50000 + 100000 * n

    # Here we calculate the required probability for this test case.
    p = 2 / num_of_n

    print("*** " + "Very Supercritical" + " Case, with " + str(num_of_n) + " Vertices and a p of: " + str(p) + " ***")
    initialize_test_for_case("Very Supercritical", num_of_n, p)
