# Agent based Macroeconomics
We will provide a summary of a model presented by Lengnick, M. (2013), who is a researcher in this field. We will also provide a framework using the Python programming language. This modeling and structure allow us to examine the desired results by changing the parameters.

## The model
**ACE** (Agent-based Computational Economics) models are divided into two categories. The first category tries to mimic real-world economies in a highly detailed way, such as the ***EURACE*** project that models the European economy. The second category consists of stylized models that abstract from real economies in a number of ways. They contain only a small number of different agent types and interaction rules. 

The model presented in the document belongs to the second category. The most influential models of this category are those of Wright, Russo et al., Dosi et al., and Gaffeo et al. Both D2008 and G2008 distinguish between three types of agents and index time by periods only, while the model presented in the paper indexes time by days and months to allow different actions to take place in different time intervals. The model at hand also follows the ACE methodology more rigorously: the agents' rules depend on purely local knowledge and not on any aggregate statistic. All transactions that occur in the model are explicitly taking place between individuals: there is always one particular agent being the buyer and one being the seller.

In contrast, D2008 have parts of their transactions carried out at the aggregate level. The model presented in the paper follows Dosi et al. and Gaffeo et al. in a number of aspects, but differs in that it analyzes growth as a result of R&D and is concerned with basic macroeconomic relations in a non-growth environment. It makes use of only two different types of agents: **households** and **firms**.

### Model considerations
in this model for generate a world that agents can do action in it, we consider some propertise:
Here are the key points of the text you provided in bullet form:

- The model covers a pure market economy without a government or central bank.
- Households and firms are fixed in number and infinitely lived.
- Production technology is also fixed.
- The fundamental time unit is days, while 21 coherent days are called a month.
- Consumption goods are bought daily while labor is bought monthly.
- Agents are characterized by loyalty to trading partners of former periods.
- The model advances this feature by explicitly stating a network of relationships among agents.
- All transactions are performed between individual agents throughout this network.
- Households have trading relations with 7 different firms (type A connections) for buying consumption goods and one firm for which they work (type B connection).
- Firms can have an unlimited amount of both types of trading relations.
- A type A and a type B connection can exist between the same household–firm-pair.
- The aggregate of all agents is connected by a bipartite network of trading relationships.
- In the short run, this network is fixed, but over time, agents cut unsatisfying trading connections to create other more beneficial ones.


- Each household has two properties: the reservation wage ωh and the liquidity mh.
- The reservation wage defines a minimal claim on labor income, but households might work for less than ωh under specific circumstances.
- The liquidity determines the amount of monetary units the household currently possesses and is changed each time the household performs a transaction.
- Current liquidity equals the sum of all past income minus the sum of all past spendings plus the initial endowment with liquidity.
- Firms also have the liquidity property mf, inventory if, a goods price pf, and a wage rate wf.
- Every household inelastically supplies one unit of labor (lh = 1).
- Households have limited knowledge and only know the prices of firms they have type A connections with and the wage rate of their employer.
- Firms do not know prices or wages of any competitor, so all knowledge is purely local and the law of one price does not necessarily apply.

## References
[1] Lengnick, M. (2013). Agent-based macroeconomics: A baseline model. Journal of Economic Behavior & Organization, 86, 102-120. https://doi.org/10.1016/j.jebo.2012.12.021
