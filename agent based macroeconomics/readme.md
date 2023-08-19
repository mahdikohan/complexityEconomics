# Agent based Macroeconomics
We will provide a summary of a model presented by Lengnick, M. (2013), who is a researcher in this field. We will also provide a framework using the Python programming language. This modeling and structure allow us to examine the desired results by changing the parameters.

<p align="center">
  <img src="https://github.com/mahdikohan/complexityEconomics/blob/5955d0e58ab01f00695afb6b68b10b8f3211935f/agent%20based%20macroeconomics/images/the%20circular%20flow.png" alt="Lorenz attractor" width="600">
</p>
<p align="center">Figure 1: A circular flow of income is an economic model</p>

## The model
**ACE** (Agent-based Computational Economics) models are divided into two categories. The first category tries to mimic real-world economies in a highly detailed way, such as the ***EURACE*** project that models the European economy. The second category consists of stylized models that abstract from real economies in a number of ways. They contain only a small number of different agent types and interaction rules. 

The model presented in the document belongs to the second category. The most influential models of this category are those of Wright, Russo et al., Dosi et al., and Gaffeo et al. Both D2008 and G2008 distinguish between three types of agents and index time by periods only, while the model presented in the paper indexes time by days and months to allow different actions to take place in different time intervals. The model at hand also follows the ACE methodology more rigorously: the agents' rules depend on purely local knowledge and not on any aggregate statistic. All transactions that occur in the model are explicitly taking place between individuals: there is always one particular agent being the buyer and one being the seller.

In contrast, D2008 have parts of their transactions carried out at the aggregate level. The model presented in the paper follows Dosi et al. and Gaffeo et al. in a number of aspects, but differs in that it analyzes growth as a result of R&D and is concerned with basic macroeconomic relations in a non-growth environment. It makes use of only two different types of agents: **households** and **firms**.

### Model considerations
in this model for generate a world that agents can do action in it, we consider some propertise:
Here are the key points of the text which provided in bullet form:

- The model covers a pure market economy **without a government** or **central bank**.
- Exclude growth in economics
  - Households and firms are fixed in number and infinitely lived.
  - Production technology is also fixed.
- The fundamental time unit is **days**, while **21** coherent days are called a **month**.
- Consumption goods are bought **daily** while labor is bought **monthly**.
- Agents are characterized by loyalty to trading partners of former periods.
- The model advances this feature by explicitly stating a network of relationships among agents.
- All transactions are performed between individual agents throughout this network.
- Firms can have an unlimited amount of both types of trading relations.
- In the short run, this network is fixed, but over time, agents cut unsatisfying trading connections to create other more beneficial ones.
- Each household has two properties: the reservation wage **$`\omega_{h}`$** and the liquidity **$`m_{h}`$**.
- The reservation wage defines a minimal claim on labor income, but households might work for less than **$`\omega_{h}`$** under specific circumstances.
- The liquidity determines the amount of monetary units the household currently possesses and is changed each time the household performs a transaction.
- Current liquidity equals the sum of all past income minus the sum of all past spendings plus the initial endowment with liquidity.

$$
m_{h,t} = m_{h,t-1} + Income_{t-1} - Spending_{t-1}
$$
- Firms also have the liquidity property **$`m_f`$**, inventory **$`i_f`$**, a goods price **$`p_f`$**, and a wage rate **$`w_f`$**.
- Every household inelastically supplies one unit of labor ($`l_h = 1`$).
- Households have limited knowledge and only know the prices of firms they have connections with them and the wage rate of their employer.
- Firms do not know prices or wages of any competitor, so all knowledge is purely local and the law of one price does not necessarily apply.

#### Beginning of a month

- At the beginning of a month, each firm has to decide on how to set its wage rate based on past success or failure to find workers at the offered wage rate.
- The firm increases or decreases its wage rate based on whether it was able to fill all positions with workers in the last month.
- Wage adjustment is performed by multiplying the current wage with a growth rate that is **idiosyncratic** [* an unusual habit or way of behaving that someone has] and drawn from a **uniform distribution**.
- The decision whether to change the price or the number of employees is based on a comparison of the current level of inventories with the most recent demand.
- If the inventory has fallen below a certain level, a new open position is created to raise production. If inventories are above a certain level, a worker is fired.
- Hiring decisions lead to an immediate offering of a new position, while firing decisions are implemented with a lag of one month.
- The decision on changing the goods price is based on whether the firm is confronted with an unsatisfying level of inventories.
- If current inventories are below or above certain critical bounds, the firm considers increasing or decreasing its price, respectively.
- Prices are raised or decreased as long as they are within certain upper and lower bar values relative to marginal costs.
- Prices are adjusted according to a formula where the growth rate is idiosyncratic and drawn from a uniform distribution.
- Similar to Calvo (1983) firms set the newly determined price $`p^{new}_f`$ only with a probability $`\theta < 1`$.
- After all firms have formed decisions, it is the households’ turn to search for more beneficial trading connections.
- Households are picked in a random order to seek for new network connections that are more beneficial than existing ones.
- With a certain probability, each household picks one randomly determined firm from the subset of all firms he has a connection with and one randomly determined firm from those he has no such connection with.
- The probability of picking the latter out of the set of all possible firms is proportional to the firm’s size, measured in employees.
- If the price of the latter is at least a certain percentage lower than that of the former, the existing connection is removed and the new one is established.
- This procedure represents the search of households for cheaper places to buy.
- The household might have been demand constrained during the last month, i.e. one or more of the firms he wanted to buy from were not able to satisfy his demand fully.
- If this is the case, the household randomly determines one of those firms with a probability proportional to the extent of the restriction.
- Household cuts the connection to this firm and replaces it with a connection to a new one.
- This procedure represents the search for firms that are able to satisfy the demand fully.
- In analogy to the above search mechanism, this procedure is only executed with a certain probability.
- The goods demand that one individual firm encounters is negatively correlated with its price and with its failure to satisfy past demand.
- If the household is unemployed, he visits a randomly chosen firm to check whether there is an open position.
- If the firm indeed offers an open position and pays a wage that is higher than the household’s currently received wage, the position is accepted and a new connection between the household and the firm is created.
- If the firm offers no vacancy or the wage it pays is too small, the search process is repeated until a total number of firms have been visited.
- An employed household might end up working for less than his reservation wage if his employer has decided to decrease wages.
- In such a case, households do not quit immediately but instead intensify their search effort for another job that satisfies certain conditions.
- As a result, we have three different intensities to search for vacancies: employees who are satisfied with their job show the least search effort in the labor market.
- Unemployed households show the highest search effort since they visit more than one firm per month.
- Households have to decide how much liquidity to spend for the purchase of consumption goods and how much to save.
- Following G2008, the interest on savings is normalized to 0.
- According to empirical evidence and theory, consumption expenditure increases with personal wealth but at a decaying rate.
- Consumption (and thus also savings) depends only on wealth and not on the interest rate. Savings are thus due to a precautionary motive.
- Since households receive income on a monthly basis, the decision of dividing it on consumption and savings is also performed monthly.
- To avoid inconsistent planning behavior that violates the budget constraint, the equation is changed.

<p align="center">
  <img src="https://github.com/mahdikohan/complexityEconomics/blob/c91e90314f693efe588a7f5653f84529b44d3db4/agent%20based%20macroeconomics/images/Flow%20chart%20of%20firms%20s%20decision%20procedure.PNG" alt="" width="720">
</p>
<p align="center">Figure 2:  Flow chart of firms’s decision procedure</p>


#### The lapse of a day
- After the above steps have been performed, the transactions of the first day begin.
- Households are picked in a random order to execute their goods demand.
- Since planned demand $`c^r_h`$ has been determined for a complete month, but transactions are taking place daily, we have to bring $`c^r_h`$ from a monthly to a daily basis.
- The most simple and straightforward way to do so is to assume that $`c^r_h`$ is distributed equally over the days of the month.
- Each household visits one randomly determined firm of those he has a connection with.
- If that firm’s inventories are high enough to satisfy his daily demand of $`c^r_{h}/21`$ and the household’s liquidity is high enough to pay for the goods, the transaction will be performed.
- The household’s liquidity is reduced by the purchasing costs, while the firm’s liquidity is raised by the same amount and its inventories are reduced by $`c^r_{h}/21`$.
- If the household cannot afford to buy the planned amount of goods, his demand is reduced to the highest possible amount.
- If the firm’s inventories are lower than the household’s demand, the transaction is performed at the highest possible amount of it. Thus inventories can never become negative.
- The household tries to satisfy the remaining demand by repeating the buying process with another firm. This process is stopped after $`n`$ firms have been asked or at least 95 percent of the planned demand has been satisfied. Eventually, remaining demand vanishes.
- Next, each firm produces according to a production function where $`l_f`$ is the number of workers the firm employs and $`\lambda`$ is a positive technology parameter.
- Following G2008, we assume a production technology that is a linear function of labor input.
- The firm’s inventory is increased by the produced goods.
- After all households and firms have performed their daily actions, the next day starts.

#### End of the month
- After all 21 working days are performed, the month ends.
- Firms use the liquidity they own at the end of a month for three different purposes: pay wages, build a buffer for bad times, and pay profits.
- First, all firms pay their workers a wage of $`w_f`$: the firm’s liquidity is reduced by $`w_f.l_f`$ while the liquidity of each household employed by that firm is raised by $`w_f`$.
- Second, if the firm has liquidity remaining after the payout of wages, it keeps a fraction as a buffer for possibly negative future profits. This liquidity buffer ($`m^{buffer}_{f,t}`$) is given relative to labor costs.
- Third, all remaining liquidity of the firm is distributed as profit among all households. Rich households have higher claims on firms’ profits than poor ones. Therefore each household receives a share of aggregate profits that is proportional to his current liquidity.
- In some cases, it might happen that the firm made losses during the month. As a first option, the firm bridges this problematic situation by not paying any profit and reducing the liquidity buffer while keeping the wage payments unchanged.
- However, in some rare cases, the losses might be so large that even with a reduction of $`m^{buffer}_{f,t}`$ down to zero, the labor costs are unaffordable. In this situation, we assume that the firm’s employees accept an immediate wage cut that is sufficient to keep the firm operating.
- As a next step, households adjust their reservation wage depending on their currently received labor income. If the labor income exceeds a household's reservation wage, $`w_h`$ is raised to the level of the received labor income. If the labor income is lower than $`w_h`$, the reservation wage is not changed. Instead, the household intensifies his search for a better-paid job.
- If a household has been unemployed during the last month, his reservation wage for the next month is reduced by 10 percent.
- The month ends and the next one begins.

### Equations
Production function, $`\lambda`$ is a positive technology parameter and $`l_f`$ is firm labor count.

$$
f(l_f)=\lambda.l_f
$$

## References
[1] Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior & Organization, 86, 102-120. https://doi.org/10.1016/j.jebo.2012.12.021
