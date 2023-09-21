import networkx as nx
import random
import matplotlib.pyplot as plt
import math

plot_state = True
report_state = True

# Create an empty graph
G = nx.Graph()
# Define the number of firms and households
num_firms = 100
num_households = 1000
num_steps = 300  # Number of simulation steps
_lambda = 3     # Fix of technology
phi = 0.25      # demand production relation production = phi * demand




# Initialize households with attributes and add them to the graph
for household_id in range(num_households):
    wage = random.uniform(2000, 6000)
    liquidity = random.uniform(50000, 300000)
    demand = random.uniform(20, 100)
    household_attrs = {
        "type": "household",
        "wage": wage,
        "liquidity": liquidity,
        "demand": demand,
        "labors":[]
    }
    G.add_node(f"Household_{household_id}", **household_attrs)

# Initialize firms with attributes and add them to the graph
for firm_id in range(num_firms):
    wage = random.uniform(30000, 70000)
    liquidity = random.uniform(10000000, 50000000)
    production = random.uniform(100, 500)
    price = random.uniform(10,20)
    low_production = random.randint(1, 100)
    production_boundray = [low_production, random.randint(low_production + 1, 550)]
    recent_demand =random.uniform(20, 100)
    recent_production = random.uniform(100, 500)

    firm_attrs = {
        "type": "firm",
        "wage": wage,
        "liquidity": liquidity,
        "production": production,
        "recent_production": recent_production,
        "production_boundary": production_boundray,
        "price": price,
        "recent_demand": recent_demand
    }
    G.add_node(f"Firm_{firm_id}", **firm_attrs)





# ============================ recruitment ==============================
j = 0
for firm_id in range(num_firms):
    # Randomly recruit a number of households
    i = random.randint(5,math.floor(num_households/num_firms)+1)
    if j<num_households:
        for recruit in range(j,j+i):
            G.add_edge(f"Firm_{firm_id}", f"Household_{recruit}")
    j = j+i


# set known employees
for households_id in range(num_households):
    connected_firm = random.sample(range(0, num_firms), math.floor(num_firms/2))
    G.nodes[f"Household_{recruit}"]["recent_demand"] = connected_firm


if plot_state==True:
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()


wage_households_1 = []
production_firm_1 = []
unemployment_rate = []

# Simulation loop
for step in range(num_steps):
    print(f"Step {step + 1}: Starting")
    print('====================================')

    # each households check some firms wage
    for household_id in range(num_households):
        # search a job position
        for firm_id in random.sample(range(0, num_firms), math.floor(num_firms/2)):
            if G.nodes[f"Firm_{firm_id}"]['liquidity'] < 0:
                G.remove_edges_from(list(G.edges(f"Firm_{firm_id}")))
            elif G.degree(f"Household_{household_id}") > 0 and (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                # print(f'new connection household_{household_id}, firm_{firm_id}')
                G.remove_edges_from(list(G.edges(f"Household_{household_id}")))
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']
            elif (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']
        if G.degree(f"Household_{household_id}") == 0:
            if G.nodes[f"Household_{household_id}"]['wage'] > 0:
                G.nodes[f"Household_{household_id}"]['wage'] = 0.9 * G.nodes[f"Household_{household_id}"]['wage']
                # =============================================================================
                # print(f'unemployment new connection household_{household_id}, firm_{firm_id}')
                # if G.nodes[f"Firm_{firm_id}"]['wage'] > 0:
                #     G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                #     G.nodes[f"Firm_{firm_id}"]['wage'] = G.nodes[f"Household_{household_id}"]['wage']



    # production which is related to number of labor in firms
    for firm_id in range(num_firms):
        # adjust production
        G.nodes[f"Firm_{firm_id}"]["recent_production"] = phi * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
        # new production
        recent_production = G.nodes[f"Firm_{firm_id}"]["recent_production"]
        G.nodes[f"Firm_{firm_id}"]['production'] = recent_production + _lambda*(G.degree(f"Firm_{firm_id}"))    



    # pay wage and adjust wage households
    for firm_id in range(num_firms):
        liquidity = G.nodes[f"Firm_{firm_id}"]["liquidity"]
        # print(f"liquidity of Firm_{firm_id}: {liquidity}")
        if liquidity > 0:
            labors = G.neighbors(f"Firm_{firm_id}")
            G.nodes[f"Firm_{firm_id}"]['wage'] = wage
            for labor in labors:
                G.nodes[f"Firm_{firm_id}"]["liquidity"] -= wage
                G.nodes[labor]["liquidity"] += wage
                if labor=="Household_6":
                    wage_households_1.append(G.nodes[labor]["liquidity"])
            if firm_id == 6:
                production_firm_1.append(G.nodes[f"Firm_{firm_id}"]["production"])
        else:
            print(f'Firm_{firm_id} Bankrupt')





    # preparing for update recent demand
    for firm_id in connected_firm:
        G.nodes[f'Firm_{firm_id}']['recent_demand'] = 0

    # consumption
    for household_id in range(num_households):
        # random selection for connection
        connected_firm = random.sample(range(0, num_firms), math.floor(num_firms/2))
        total_price = 0
        for firm_id in connected_firm:
            total_price += G.nodes[f'Firm_{firm_id}']['price']
        avg_price = total_price/len(connected_firm)
        # buy things
        for firm_id in connected_firm:
            demand = ((G.nodes[f'Household_{household_id}']['liquidity'] / avg_price)**0.9)
            # print('==============demand of consumer==============')
            # print(G.nodes[f'Household_{household_id}'], f'price: {avg_price}')
            # input()
            consumption = demand * avg_price
            G.nodes[f'Firm_{firm_id}']['recent_demand'] += demand
            # if type(consumption)==complex:
                # print(f"consumprion is complex Household_{household_id}")
                # print(G.nodes[f'Household_{household_id}'])
                # input()
            if type(consumption)!= complex and consumption > 0:
                firm_production = G.nodes[f'Firm_{firm_id}']['production']
                if type(firm_production) != complex and firm_production > 0:
                    if G.nodes[f'Firm_{firm_id}']['production'] > demand:
                        G.nodes[f'Household_{household_id}']['liquidity'] -= consumption
                        G.nodes[f'Firm_{firm_id}']['liquidity'] += consumption
                    elif G.nodes[f'Firm_{firm_id}']['production'] < demand:
                        consumption -= G.nodes[f'Household_{household_id}']['liquidity'] 
                        G.nodes[f'Firm_{firm_id}']['liquidity'] += consumption
                        G.nodes[f'Firm_{firm_id}']['production'] = 0
                else:
                    break
                    print(f"Firm_{firm_id}: production is zero")
            else:
                print(f"Household_{household_id}: consumption is zero")
                break

    unem_c = 0
    for household_id in range(num_households):
        if G.degree(f"Household_{household_id}")==0:
            unem_c += 1
    
    u_r = unem_c / num_households * 100
    unemployment_rate.append(u_r)
    print(f'unemployment rate: {u_r} %')
    print('==============================')

    # adjust price:
    for firm_id in range(num_firms):
        pass

    
if plot_state==True:
    plt.plot(wage_households_1)
    plt.title('Wage')
    plt.show()

    plt.plot(production_firm_1)
    plt.title('Production')
    plt.show()



    # Visualize the graph to show recruitment
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'yellow' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()


if report_state == True:  
    print(f'unemployment rate: {sum(unemployment_rate)/len(unemployment_rate)} %')
