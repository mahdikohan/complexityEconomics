import networkx as nx
import random
import matplotlib.pyplot as plt
import math

plot_state = True
graph_state = True
report_state = False

# Create an empty graph
G = nx.Graph()
# Define the number of firms and households
minimum_wage = 0
maximum_wage = 10000
num_firms = 100
num_connected_firms = 7
num_households = 1000
num_steps = 100             # Number of simulation steps
num_days = 21               # Number of days
_lambda = 3                 # Fix of technology
# phi = 0.25                # demand production relation production = phi * demand
init_invest = 2             # initial investment for 6 monthes
theta = 0.75                # imilar to Calvo (1983) firms set the newly determined price only with a probability
thi_up = 1.15
thi_down = 1.025
phi_up = 1
phi_down = 0.25

nu = 0.02
delta = 0.019





# Initialize households with attributes and add them to the graph
for household_id in range(num_households):
    h_wage = 1200
    liquidity = random.uniform(3000, 5000)
    demand = random.uniform(20, 100)
    household_attrs = {
        "type": "household",
        "wage": h_wage,
        "liquidity": liquidity,
        "demand": demand,
        "recent_demand_status": None, # complete or uncomplete
        "labors":0
    }
    G.add_node(f"Household_{household_id}", **household_attrs)

# Initialize firms with attributes and add them to the graph
for firm_id in range(num_firms):
    f_wage = 1000
    recent_wage = random.uniform(3000, 7000)
    liquidity = random.uniform(100000, 500000)
    production = random.uniform(100, 500)
    price = random.uniform(10,20)
    low_production = random.randint(1, 100)
    low_price = random.randint(1,10)
    price_boundary = [low_price, random.randint(low_price + 1,25)]
    production_boundary = [low_production, random.randint(low_production + 1, 550)]
    recent_demand =random.uniform(20, 100)

    firm_attrs = {
        "type": "firm",
        "wage": f_wage,
        "liquidity": liquidity,
        "production": production,
        "recent_production": production,
        "price_boundary": price_boundary,
        "production_boundary": production_boundary,
        "price": price,
        "demand":0,
        "reserve": 0,
        "recent_labors": 0,
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
            G.nodes[f"Household_{recruit}"]["wage"] = G.nodes[f"Firm_{firm_id}"]["wage"]
    j = j+i
    G.nodes[f"Firm_{firm_id}"]["recent_labors"] = G.degree(f"Firm_{firm_id}")



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
                    print(f"Firm_{firm_id}", f"Household_{household_id}")
                    hire_number -= 1
                    g.nodes[f"Household_{household_id}"]["wage"] = f_wage
    return g

def update_h_wages(g,firm_id):
    labors = list(g.neighbors(f"Firm_{firm_id}"))
    update_wage = g.nodes[f"Firm_{firm_id}"]["wage"]
    for l in labors:
        g.nodes[l]["wage"] = update_wage
    return g

wage_households_test = []
production_firm_test = []
reservation_firm_test = []
total_production_firm_test = []
total_reservation_firm_test = []
liquidity_households_test = []
unemployment_rate = []
employment_rate = []
Bankrupt_rate = []
header = 0

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

    # Adjust wage households
    for firm_id in range(num_firms):
        wage = G.nodes[f"Firm_{firm_id}"]["wage"]
        if wage > minimum_wage and wage < maximum_wage:
            G.nodes[f"Firm_{firm_id}"]["recent_wage"] = wage
            if G.nodes[f"Firm_{firm_id}"]["free_position"] > 0:
                # this means firm is unsuccessful in hiring
                G.nodes[f"Firm_{firm_id}"]["wage"] = wage * (1 + random.uniform(0,delta))
                G = update_h_wages(G,firm_id)
            else:
                # this means firm is successful in hiring
                G.nodes[f"Firm_{firm_id}"]["wage"] = wage * (1 - random.uniform(0,delta))
                G = update_h_wages(G,firm_id)
    

    # Price and inventory boundary
    for firm_id in range(num_firms):
        # update recent demand by previous month
        G.nodes[f"Firm_{firm_id}"]["recent_demand"] = G.nodes[f"Firm_{firm_id}"]['demand']
        G.nodes[f"Firm_{firm_id}"]["demand"] = 0
        # update recent production
        # G.nodes[f"Firm_{firm_id}"]["recent_production"] = G.nodes[f"Firm_{firm_id}"]["production"]
        G.nodes[f"Firm_{firm_id}"]["recent_production"] = G.nodes[f"Firm_{firm_id}"]["reserve"]
        # G.nodes[f"Firm_{firm_id}"]["production"] = 0
        # Adjust inventory(production) boundary
        production_boundary_adj_up = phi_up * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
        production_boundary_adj_down = phi_down * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
        G.nodes[f"Firm_{firm_id}"]["production_boundary"] = [production_boundary_adj_down,production_boundary_adj_up]
        # Adjust price boundary
        # # price is related to marginal cost
        recent_wage_price_adj = G.nodes[f"Firm_{firm_id}"]["recent_wage"]
        wage_price_adj = G.nodes[f"Firm_{firm_id}"]["wage"]
        # # calculation of marginal cost by difference of labor costs respect to last month
        dc_price_adj = (G.degree(f"Firm_{firm_id}") * wage_price_adj) - (G.nodes[f"Firm_{firm_id}"]["recent_labors"] * recent_wage_price_adj)
        # dq_price_adj = G.nodes[f"Firm_{firm_id}"]["production"] - G.nodes[f"Firm_{firm_id}"]["recent_production"]
        dq_price_adj = G.nodes[f"Firm_{firm_id}"]["reserve"] - G.nodes[f"Firm_{firm_id}"]["recent_production"]
        if dq_price_adj != 0 and dc_price_adj != 0:
            price_up_adj = thi_up * (dc_price_adj/dq_price_adj)
            price_down_adj = thi_down * (dc_price_adj/dq_price_adj)
            G.nodes[f"Firm_{firm_id}"]["price_boundary"] = [price_down_adj,price_up_adj]





    # Search new position with households
    for firm_id in range(num_firms):
        G = hiring_by_firm(G,firm_id)
    for household_id in range(num_households):
        if G.degree(f"Household_{household_id}") == 0 and (G.nodes[f"Firm_{firm_id}"]["free_position"] > 0) and \
              (G.nodes[f"Firm_{firm_id}"]["wage"] > G.nodes[f"Household_{household_id}"]["wage"]):
            if G.nodes[f"Household_{household_id}"]["wage"] > minimum_wage:
                G.nodes[f"Household_{household_id}"]["wage"] = G.nodes[f"Household_{household_id}"]["wage"] * (1 - random.uniform(0,0.25))
                G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                G.nodes[f"Firm_{firm_id}"]["free_position"] -= 1
                G.nodes[f"Household_{household_id}"]["wage"] = G.nodes[f"Firm_{firm_id}"]["wage"]
        else:
            # Search a job position
            labors_part_job_position = G.nodes[f"Household_{household_id}"]["labors"]
            # effort = len(labors_part_job_position)
            effort = 1
            for firm_id in random.sample(labors_part_job_position, effort):
                if G.nodes[f"Firm_{firm_id}"]["liquidity"] < 0:
                    G.remove_edges_from(list(G.edges(f"Firm_{firm_id}")))
                elif G.degree(f"Household_{household_id}") > 0 and \
                    G.nodes[f"Firm_{firm_id}"]["free_position"] > 0 and \
                    ((G.nodes[f"Firm_{firm_id}"]["wage"]) > (G.nodes[f"Household_{household_id}"]["wage"])):
                    firm_of_labor_link = list(G.edges(f"Household_{household_id}"))
                    G.remove_edges_from(firm_of_labor_link)
                    G.nodes[firm_of_labor_link[0][1]]["free_position"] += 1
                    G.add_edge(f"Household_{household_id}",f"Firm_{firm_id}")
                    G.nodes[f"Firm_{firm_id}"]["free_position"] -= 1
                    G.nodes[f"Household_{household_id}"]["wage"] = G.nodes[f"Firm_{firm_id}"]["wage"]

        





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
            # # Adjust production
            # G.nodes[f"Firm_{firm_id}"]["recent_production"] = phi * G.nodes[f"Firm_{firm_id}"]["recent_demand"]
            # # New production
            # G.nodes[f"Firm_{firm_id}"]["production"] += _lambda*(G.degree(f"Firm_{firm_id}"))
            G.nodes[f"Firm_{firm_id}"]["reserve"] += _lambda*(G.degree(f"Firm_{firm_id}"))



            
            if firm_id == 1:  
                attributes_to_print = list(G.nodes[f"Firm_{firm_id}"].keys())
                values_to_print = [G.nodes[f"Firm_{firm_id}"][attr] for attr in attributes_to_print]
                column_names = ','.join(attributes_to_print)
                values_to_print.append(G.degree(f'Firm_{firm_id}'))
                values_to_print.append(step)
                values = ','.join(map(str, values_to_print))
                
                # print(column_names)
                # print(values)

                # print(list(G.nodes[f'Firm_1'].keys()))
                with open('log.csv','+a') as f:
                    if header == 0:
                        f.write(column_names+",labors,step"+"\n")
                        header +=1
                    f.write(values.replace(',[',',"[').replace('],',']",')+"\n")






            # Adjust production
            if G.degree(f"Firm_{firm_id}") > 1:
                # reset state
                G.nodes[f"Firm_{firm_id}"]["free_position"] = 0


                # firm_production_adj_part = G.nodes[f"Firm_{firm_id}"]["production"]
                firm_production_adj_part = G.nodes[f"Firm_{firm_id}"]["reserve"]
                firm_price_adj_part = G.nodes[f"Firm_{firm_id}"]["price"]
                firm_low_production_adj_part = G.nodes[f"Firm_{firm_id}"]["production_boundary"][0]
                firm_high_production_adj_part = G.nodes[f"Firm_{firm_id}"]["production_boundary"][1]
                firm_low_price_adj_part = G.nodes[f"Firm_{firm_id}"]["price_boundary"][0]
                firm_high_price_adj_part = G.nodes[f"Firm_{firm_id}"]["price_boundary"][1]
                probability_Calvo = random.random()
                if firm_production_adj_part > firm_high_production_adj_part:
                    fire_adj_part = random.choice(list(G.neighbors(f"Firm_{firm_id}")))
                    # Fire with one month delay
                    if G.nodes[f"Firm_{firm_id}"]["free_position"] == 0:
                        G.nodes[f"Firm_{firm_id}"]["free_position"] -= 1
                    if probability_Calvo > 1-theta:
                        if firm_price_adj_part > firm_high_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]["price"] = firm_price_adj_part * (1 - random.uniform(0,nu))
                        elif firm_price_adj_part < firm_low_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]["price"] = firm_price_adj_part * (1 + random.uniform(0,nu))
                elif firm_production_adj_part < firm_low_production_adj_part:
                    # Hiring immediately
                    if G.nodes[f"Firm_{firm_id}"]["free_position"] == 0:
                        G.nodes[f"Firm_{firm_id}"]["free_position"] += 1
                    # elif G.nodes[f"Firm_{firm_id}"]["free_position"] == 1:
                    if G.nodes[f"Firm_{firm_id}"]["wage"]>minimum_wage and G.nodes[f"Firm_{firm_id}"]["wage"]<maximum_wage:
                        G.nodes[f"Firm_{firm_id}"]["wage"] = G.nodes[f"Firm_{firm_id}"]["wage"] * (1 + random.uniform(0,delta))
                        G = update_h_wages(G,firm_id)
                    G = hiring_by_firm(G, firm_id)
                    if probability_Calvo > 1-theta:
                        if firm_price_adj_part > firm_high_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]["price"] = firm_price_adj_part * (1 - random.uniform(0,nu))
                        elif firm_price_adj_part < firm_low_price_adj_part:
                            G.nodes[f"Firm_{firm_id}"]["price"] = firm_price_adj_part * (1 + random.uniform(0,nu))

        # Report about daily unemployement
        if graph_state == True:
            c_num_unem = 0
            for household_id in range(num_households):
                if G.degree(f"Household_{household_id}") == 0:
                    c_num_unem += 1
            unemployment_rate.append(c_num_unem)





        


        # Consumption
        for household_id in range(num_households):
            connected_firm = G.nodes[f"Household_{household_id}"]["labors"]
            total_price = 0
            for firm_id in connected_firm:
                total_price += G.nodes[f"Firm_{firm_id}"]["price"]
            avg_price = total_price / len(connected_firm)
            # We did it for uniform distribution of sellers
            sample_firms = random.sample(connected_firm, len(connected_firm))
            # Buy things
            
            demand = min(((G.nodes[f"Household_{household_id}"]["liquidity"] / avg_price) ** 0.9),\
                        (G.nodes[f"Household_{household_id}"]["liquidity"] / avg_price)) / num_days
            for firm_id in sample_firms:



                # recent demand
                G.nodes[f"Firm_{firm_id}"]['demand'] += demand



                consumption = demand * G.nodes[f"Firm_{firm_id}"]["price"]
                if consumption > 0:
                    firm_production = G.nodes[f"Firm_{firm_id}"]["reserve"]
                    if firm_production > 0:
                        if G.nodes[f"Firm_{firm_id}"]["reserve"] >= demand:
                            if G.nodes[f"Household_{household_id}"]["liquidity"] > consumption:
                                G.nodes[f"Household_{household_id}"]["liquidity"] -= consumption
                                G.nodes[f"Firm_{firm_id}"]["reserve"] -= demand
                                G.nodes[f"Firm_{firm_id}"]["liquidity"] += consumption
                                demand = 0
                            elif G.nodes[f"Household_{household_id}"]["liquidity"] < consumption:
                                G.nodes[f"Firm_{firm_id}"]["reserve"] -= demand
                                G.nodes[f"Firm_{firm_id}"]["liquidity"] += G.nodes[f"Household_{household_id}"]["liquidity"]
                                G.nodes[f"Household_{household_id}"]["liquidity"] = 0
                                demand = 0
                        elif G.nodes[f"Firm_{firm_id}"]["reserve"] < demand:
                            if G.nodes[f"Household_{household_id}"]["liquidity"] > consumption:
                                share_of_consumption = G.nodes[f"Firm_{firm_id}"]["reserve"] * G.nodes[f"Firm_{firm_id}"]["price"]
                                G.nodes[f"Household_{household_id}"]["liquidity"] -= share_of_consumption
                                G.nodes[f"Firm_{firm_id}"]["reserve"] = 0
                                G.nodes[f"Firm_{firm_id}"]["liquidity"] += share_of_consumption
                                demand -= (share_of_consumption / G.nodes[f"Firm_{firm_id}"]["price"])
                            elif G.nodes[f"Household_{household_id}"]["liquidity"] < consumption:
                                share_of_demand = G.nodes[f"Household_{household_id}"]["liquidity"] / G.nodes[f"Firm_{firm_id}"]["price"]
                                if G.nodes[f"Firm_{firm_id}"]["reserve"] > share_of_demand:
                                    G.nodes[f"Firm_{firm_id}"]["reserve"] -= share_of_demand
                                    G.nodes[f"Firm_{firm_id}"]["liquidity"] += G.nodes[f"Household_{household_id}"]["liquidity"]
                                    G.nodes[f"Household_{household_id}"]["liquidity"] = 0
                                    demand = 0
                                elif G.nodes[f"Firm_{firm_id}"]["reserve"] < share_of_demand:
                                    share_of_consumption = G.nodes[f"Firm_{firm_id}"]["reserve"] * G.nodes[f"Firm_{firm_id}"]["price"]
                                    G.nodes[f"Household_{household_id}"]["liquidity"] -= share_of_consumption
                                    G.nodes[f"Firm_{firm_id}"]["reserve"] = 0
                                    G.nodes[f"Firm_{firm_id}"]["liquidity"] += share_of_consumption
                                    demand -= (share_of_consumption / G.nodes[f"Firm_{firm_id}"]["price"])
                    else:
                        # print(f"Firm_{firm_id}: production is zero")
                        # print(G.nodes[f"Firm_{firm_id}"])
                        # input()
                        break
                else:
                    # print(f"Household_{household_id}:h consumption is zero")
                    # print(G.nodes[f"Household_{household_id}"])
                    # input()
                    break
            
            if demand == 0:
                G.nodes[f"Household_{household_id}"]['recent_demand_status'] = "complete"
            else:
                G.nodes[f"Household_{household_id}"]['recent_demand_status'] = "uncomplete"









    # pay wage
    for firm_id in range(num_firms):
        cons_liq = liquidity
        liquidity = G.nodes[f"Firm_{firm_id}"]["liquidity"]
        labors = list(G.neighbors(f"Firm_{firm_id}"))
        wage = G.nodes[f"Firm_{firm_id}"]["wage"]
        # print(f"liquidity of Firm_{firm_id}: {liquidity}")
        if liquidity > 0:
            for labor in labors:
                if G.nodes[f"Firm_{firm_id}"]["liquidity"] < (len(labors) * wage):
                    break
                G.nodes[f"Firm_{firm_id}"]["liquidity"] -= wage
                G.nodes[labor]["liquidity"] += wage
        else:
            if report_state == True:
                print(f'Firm_{firm_id} Bankrupt')
















    # fire labors with delay of one month
    for firm_id in range(num_firms):
        # check recent things count
        G.nodes[f"Firm_{firm_id}"]["recent_labors"] = G.degree(f"Firm_{firm_id}")
        while G.nodes[f"Firm_{firm_id}"]["free_position"] < 0:
            fire_adj_part = random.choice(list(G.neighbors(f"Firm_{firm_id}")))
            G.remove_edge(f"Firm_{firm_id}", fire_adj_part)
            G.nodes[f"Firm_{firm_id}"]["free_position"] += 1

            





    # Generate report for this month
    total_production = 0
    total_reservation = 0
    for firm_id in range(num_firms):
        # total_production += G.nodes[f"Firm_{firm_id}"]["production"]
        total_reservation += G.nodes[f"Firm_{firm_id}"]["reserve"]
    total_production_firm_test.append(total_production)
    
    production_firm_test.append(G.nodes["Firm_5"]["production"])
    reservation_firm_test.append(G.nodes["Firm_5"]["reserve"])
    # input()


if plot_state == True:
    plt.plot(production_firm_test)
    plt.title('production_firm_test')
    plt.show()


    plt.plot(reservation_firm_test)
    plt.title('reservation_firm_test')
    plt.show()


    plt.plot(unemployment_rate)
    plt.title('unemployment_rate')
    plt.show()

if graph_state == True:
    pos = nx.spring_layout(G)
    node_colors = ['skyblue' if G.nodes[node]['type'] == "household" else 'yellow' for node in G.nodes()]
    nx.draw(G, pos, with_labels=True, node_color=node_colors, font_color='black', node_size=800)
    plt.show()
