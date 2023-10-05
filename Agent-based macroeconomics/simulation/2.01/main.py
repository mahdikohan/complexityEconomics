import networkx as nx
import random
import matplotlib.pyplot as plt
import math

plot_state = False
graph_state = True
report_state = False

# Create an empty graph
G = nx.Graph()
# Define the number of firms and households
minimum_wage = 800
maximum_wage = 8000
num_firms = 100
num_connected_firms = 15
num_households = 1000
num_steps = 100             # Number of simulation steps
num_days = 21               # Number of days
_lambda = 3                 # Fix of technology
phi = 0.25                  # demand production relation production = phi * demand
init_invest = 2             # initial investment for 6 monthes
theta = 0.75                # imilar to Calvo (1983) firms set the newly determined price only with a probability





# Initialize households with attributes and add them to the graph
for household_id in range(num_households):
    wage = random.uniform(2000, 6000)
    liquidity = random.uniform(3000, 5000)
    demand = random.uniform(20, 100)
    household_attrs = {
        "type": "household",
        "wage": wage,
        "liquidity": liquidity,
        "demand": demand,
        "recent_demand_status": None, # complete or uncomplete
        "labors":0
    }
    G.add_node(f"Household_{household_id}", **household_attrs)

# Initialize firms with attributes and add them to the graph
for firm_id in range(num_firms):
    wage = random.uniform(3000, 7000)
    recent_wage = random.uniform(3000, 7000)
    liquidity = random.uniform(100000, 500000)
    production = random.uniform(100, 500)
    price = random.uniform(10,20)
    low_production = random.randint(1, 100)
    low_price = random.randint(1,10)
    price_boundary = [low_price, random.randint(low_price + 1,25)]
    production_boundary = [low_production, random.randint(low_production + 1, 550)]
    recent_demand =random.uniform(20, 100)
    recent_production = random.uniform(100, 500)

    firm_attrs = {
        "type": "firm",
        "wage": wage,
        "liquidity": liquidity,
        "production": production,
        "recent_production": recent_production,
        "price_boundary": price_boundary,
        "production_boundary": production_boundary,
        "price": price,
        "recent_wage": recent_wage,
        "recent_demand": recent_demand,
        "recent_hiring": "",      # satisfy or unsatisfy
        "free_position": 0
    }
    G.add_node(f"Firm_{firm_id}", **firm_attrs)





# ============================ Recruitment ============================
j = 0
for firm_id in range(num_firms):
    # Randomly recruit a number of households
    max_i = min([math.floor(G.nodes[f"Firm_{firm_id}"]["liquidity"] / G.nodes[f"Firm_{firm_id}"]["wage"] / init_invest), 10])
    i = random.randint(math.floor(max_i/2),max_i)
    if j+i < num_households:
        for recruit in range(j, j+i):
            G.add_edge(f"Firm_{firm_id}", f"Household_{recruit}")
    j = j+i


# Set known employees
for household_id in range(num_households):
    connected_firm = random.sample(range(num_firms), num_connected_firms)
    G.nodes[f"Household_{household_id}"]["labors"] = connected_firm


if plot_state == True and graph_state == True:
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'red' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()


def hiring_by_firm(g, firm_id):
    # Among unemployed  
    hire_number = g.nodes[f"Firm_{firm_id}"]["free_position"]
    if hire_number > 0:
        for household_id in range(num_households):
            if hire_number == 0:
                break
            h = g.nodes[f"Household_{household_id}"]
            f_wage = g.nodes[f"Firm_{firm_id}"]["wage"]
            if g.degree(h) == 0:
                if f_wage >= h["wage"]:
                    g.add_edge(f"Firm_{firm_id}", f"Household_{household_id}")
                    hire_number -= 1
                    g.nodes[f"Household_{household_id}"]['wage'] = f_wage

    return g


wage_households_test = []
production_firm_test = []
total_production_firm_test = []
liquidity_households_test = []
unemployment_rate = []
employment_rate = []
Bankrupt_rate = []

# Simulation loop
for step in range(num_steps):
    print(f"Step {step + 1}: Starting")

    # Start Month
        # Adjust wage rate based on past success or failure
        # Adjust price
        # Firms new position handling (fire with 1 month delay, open hire position immediately)
        # Change boundry of price with marginal cost
        # Cheapest price households connection
        # households search for open position
        # each households check some firms wage






    # Search new position with households
    for household_id in range(num_households):
        # Search a job position
        labors_part_job_position = G.nodes[f"Household_{household_id}"]["labors"]
        for firm_id in random.sample(labors_part_job_position, len(labors_part_job_position)):
            if G.nodes[f"Firm_{firm_id}"]['liquidity'] < 0:
                G.remove_edges_from(list(G.edges(f"Firm_{firm_id}")))
            elif G.degree(f"Household_{household_id}") > 0 and \
                 G.nodes[f"Firm_{firm_id}"]["free_position"] > 0 and \
                 (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                firm_of_labor_link = list(G.edges(f"Household_{household_id}"))
                G.remove_edges_from(firm_of_labor_link)
                G.nodes[firm_of_labor_link[0][1]]["free_position"] += 1
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['free_position'] -= 1
                G.nodes[f"Household_{household_id}"]['wage'] = G.nodes[f"Firm_{firm_id}"]['wage']
            elif G.nodes[f"Firm_{firm_id}"]["free_position"] > 0 and \
                 (G.nodes[f"Firm_{firm_id}"]['wage']) > (G.nodes[f"Household_{household_id}"]['wage']):
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]['free_position'] -= 1
                G.nodes[f"Household_{household_id}"]['wage'] = G.nodes[f"Firm_{firm_id}"]['wage']
        if G.degree(f"Household_{household_id}") == 0:
            if G.nodes[f"Household_{household_id}"]['wage'] > minimum_wage:
                G.nodes[f"Household_{household_id}"]['wage'] = 0.9 * G.nodes[f"Household_{household_id}"]['wage']

    





    # Cheaper places to buy
    for household_id in range(num_households):
        connected_firms = G.nodes[f"Household_{household_id}"]["labors"]
        unconnected_firms = [i for i in range(num_firms) if i not in connected_firms]
        chosen_firm = random.choice(unconnected_firms)
        for firm_id in connected_firms:
            connected_firm_price = G.nodes[f"Firm_{firm_id}"]["price"]
            if connected_firm_price > G.nodes[f"Firm_{chosen_firm}"]["price"]:
                connected_firms.remove(firm_id)
                connected_firms.append(chosen_firm)
                G.nodes[f"Household_{household_id}"]["labors"] = connected_firms
                # Report
                if report_state == True:
                    print(f"firm {firm_id} replaced by firm {chosen_firm} in households {household_id}")
                break

    



    for day in range(num_days):
        # Production which is related to number of labor in firms
        for firm_id in range(num_firms):
            # Adjust production
            G.nodes[f"Firm_{firm_id}"]["recent_production"] = phi * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
            # New production
            recent_production = G.nodes[f"Firm_{firm_id}"]["recent_production"]
            if G.degree(f"Firm_{firm_id}") > 0:
                G.nodes[f"Firm_{firm_id}"]['production'] += recent_production + _lambda*(G.degree(f"Firm_{firm_id}"))
            else:
                G.nodes[f"Firm_{firm_id}"]['production'] = 0
            

            # if report_state == True:
            if firm_id == 1:
                with open('log.txt','+a') as f:
                   f.write(f"{G.nodes[f'Firm_1']}, labors:{G.degree(f'Firm_{firm_id}')}, step:{step} \n")






            # Adjust production
            if G.degree(f"Firm_{firm_id}") > 1:
                firm_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production']
                firm_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price']
                firm_low_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production_boundary'][0]
                firm_high_production_adj_part = G.nodes[f"Firm_{firm_id}"]['production_boundary'][1]
                firm_low_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price_boundary'][0]
                firm_high_price_adj_part = G.nodes[f"Firm_{firm_id}"]['price_boundary'][1]
                if firm_production_adj_part > firm_high_production_adj_part:
                    fire_adj_part = random.choice(list(G.neighbors(f"Firm_{firm_id}")))
                    # Fire with one month delay
                    if G.nodes[f"Firm_{firm_id}"]['free_position'] > -1:
                        G.nodes[f"Firm_{firm_id}"]['free_position'] -= 1
                    probability_Calvo = random.random()
                    if probability_Calvo > 1-theta:
                        if firm_price_adj_part > firm_high_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1 - random.uniform(0.1,0.4))
                        elif firm_price_adj_part < firm_low_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1 + random.uniform(0.1,0.4))
                elif firm_production_adj_part < firm_low_production_adj_part:
                    # Hiring immediately
                    if G.nodes[f"Firm_{firm_id}"]['free_position'] < 1:
                        G.nodes[f"Firm_{firm_id}"]['free_position'] += 1
                    elif G.nodes[f"Firm_{firm_id}"]['free_position'] == 1:
                        if G.nodes[f'Firm_{firm_id}']['wage']>minimum_wage and G.nodes[f'Firm_{firm_id}']['wage']<maximum_wage:
                            G.nodes[f'Firm_{firm_id}']['wage'] = G.nodes[f'Firm_{firm_id}']['wage'] * (1.01)
                    G = hiring_by_firm(G, firm_id)
                    if probability_Calvo > 1-theta:
                        if firm_price_adj_part > firm_high_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1 - random.uniform(0.1,0.4))
                        elif firm_price_adj_part < firm_low_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]['price'] = firm_price_adj_part * (1 + random.uniform(0.1,0.4))

        # Report about daily unemployement
        if graph_state == True:
            c_num_unem = 0
            for household_id in range(num_households):
                if G.degree(f"Household_{household_id}") == 0:
                    c_num_unem += 1
            unemployment_rate.append(c_num_unem)





        


        # Consumption
        for household_id in range(num_households):
            connected_firm = G.nodes[f'Household_{household_id}']["labors"]
            total_price = 0
            for firm_id in connected_firm:
                total_price += G.nodes[f'Firm_{firm_id}']['price']
            avg_price = total_price / len(connected_firm)
            # We did it for uniform distribution of sellers
            sample_firms = random.sample(connected_firm, len(connected_firm))
            # Buy things
            demand = ((G.nodes[f'Household_{household_id}']['liquidity'] / avg_price) ** 0.9) / num_days
            for firm_id in sample_firms:
                G.nodes[f'Firm_{firm_id}']['recent_demand'] = demand
                consumption = demand * G.nodes[f'Firm_{firm_id}']['price']
                if consumption > 0:
                    firm_production = G.nodes[f'Firm_{firm_id}']['production']
                    if firm_production > 0:
                        if G.nodes[f'Firm_{firm_id}']['production'] >= demand:
                            if G.nodes[f'Household_{household_id}']['liquidity'] > consumption:
                                G.nodes[f'Household_{household_id}']['liquidity'] -= consumption
                                G.nodes[f'Firm_{firm_id}']['production'] -= demand
                                G.nodes[f'Firm_{firm_id}']['liquidity'] += consumption
                                demand = 0
                            elif G.nodes[f'Household_{household_id}']['liquidity'] < consumption:
                                G.nodes[f'Firm_{firm_id}']['production'] -= demand
                                G.nodes[f'Firm_{firm_id}']['liquidity'] += G.nodes[f'Household_{household_id}']['liquidity']
                                G.nodes[f'Household_{household_id}']['liquidity'] = 0
                                demand = 0
                        elif G.nodes[f'Firm_{firm_id}']['production'] < demand:
                            if G.nodes[f'Household_{household_id}']['liquidity'] > consumption:
                                share_of_consumption = G.nodes[f'Firm_{firm_id}']['production'] * G.nodes[f'Firm_{firm_id}']['price']
                                G.nodes[f'Household_{household_id}']['liquidity'] -= share_of_consumption
                                G.nodes[f'Firm_{firm_id}']['production'] = 0
                                G.nodes[f'Firm_{firm_id}']['liquidity'] += share_of_consumption
                                demand -= (share_of_consumption / G.nodes[f'Firm_{firm_id}']['price'])
                            elif G.nodes[f'Household_{household_id}']['liquidity'] < consumption:
                                share_of_demand = G.nodes[f'Household_{household_id}']['liquidity'] / G.nodes[f'Firm_{firm_id}']['price']
                                if G.nodes[f'Firm_{firm_id}']['production'] > share_of_demand:
                                    G.nodes[f'Firm_{firm_id}']['production'] -= share_of_demand
                                    G.nodes[f'Firm_{firm_id}']['liquidity'] += G.nodes[f'Household_{household_id}']['liquidity']
                                    G.nodes[f'Household_{household_id}']['liquidity'] = 0
                                    demand = 0
                                elif G.nodes[f'Firm_{firm_id}']['production'] < share_of_demand:
                                    share_of_consumption = G.nodes[f'Firm_{firm_id}']['production'] * G.nodes[f'Firm_{firm_id}']['price']
                                    G.nodes[f'Household_{household_id}']['liquidity'] -= share_of_consumption
                                    G.nodes[f'Firm_{firm_id}']['production'] = 0
                                    G.nodes[f'Firm_{firm_id}']['liquidity'] += share_of_consumption
                                    demand -= (share_of_consumption / G.nodes[f'Firm_{firm_id}']['price'])
                    else:
                        # print(f"Firm_{firm_id}: production is zero")
                        # print(G.nodes[f'Firm_{firm_id}'])
                        # input()
                        break
                else:
                    # print(f"Household_{household_id}:h consumption is zero")
                    # print(G.nodes[f'Household_{household_id}'])
                    # input()
                    break
            
            if demand == 0:
                G.nodes[f'Household_{household_id}']['recent_demand_status'] = "complete"
            else:
                G.nodes[f'Household_{household_id}']['recent_demand_status'] = "uncomplete"









    # pay wage
    for firm_id in range(num_firms):
        cons_liq = liquidity
        liquidity = G.nodes[f"Firm_{firm_id}"]["liquidity"]
        labors = list(G.neighbors(f"Firm_{firm_id}"))
        wage = G.nodes[f"Firm_{firm_id}"]['wage']
        # print(f"liquidity of Firm_{firm_id}: {liquidity}")
        if liquidity > 0 and liquidity > 0.6 * (len(labors) * wage):
            for labor in labors:
                if G.nodes[f"Firm_{firm_id}"]["liquidity"] < 0.6 * (len(labors) * wage):
                    break
                G.nodes[f"Firm_{firm_id}"]["liquidity"] -= wage
                G.nodes[labor]["liquidity"] += wage
        else:
            if report_state == True:
                print(f'Firm_{firm_id} Bankrupt')





     # Adjust wage households
    for firm_id in range(num_firms):
        wage = G.nodes[f"Firm_{firm_id}"]['wage']
        if wage>minimum_wage and wage<maximum_wage:
            if G.nodes[f"Firm_{firm_id}"]['free_position'] > 0:
                # this means firm is unsuccessful in hiring
                G.nodes[f"Firm_{firm_id}"]['wage'] = wage * (1.01)
            elif G.nodes[f"Firm_{firm_id}"]['free_position'] <= 0:
                # this means firm is unsuccessful in hiring
                G.nodes[f"Firm_{firm_id}"]['wage'] = wage * (0.99)










    # fire labors with delay of one month
    for firm_id in range(num_firms):
        while G.nodes[f"Firm_{firm_id}"]['free_position'] < 0:
            fire_adj_part = random.choice(list(G.neighbors(f"Firm_{firm_id}")))
            G.remove_edge(f"Firm_{firm_id}", fire_adj_part)
            G.nodes[f"Firm_{firm_id}"]['free_position'] += 1

            





    # Generate report for this month
    total_production = 0
    for firm_id in range(num_firms):
        total_production += G.nodes[f"Firm_{firm_id}"]["production"]
    total_production_firm_test.append(total_production)
    production_firm_test.append(G.nodes["Firm_5"]["production"])
    # input()


plt.plot(production_firm_test)
plt.show()


plt.plot(unemployment_rate)
plt.show()


pos = nx.spring_layout(G)
node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'yellow' for node in G.nodes()]
nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
plt.show()
