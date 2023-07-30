# El Farlo Problem
In a thought-provoking discussion of rationality in economics, the author argues that while the concept of perfect, logical, deductive rationality is useful for solving theoretical problems, it falls short in accurately describing human behavior in more complex situations. The author attributes this to two factors: the limitations of human rationality in coping with high levels of complexity and the inability of agents to rely on others to behave perfectly rationally in interactive situations. As a result, economists have been exploring alternative models of bounded rationality, with many ideas being proposed but no consensus yet reached. In contrast, psychologists have reached a reasonable agreement that humans use characteristic and predictable methods of inductive reasoning in complicated or ill-defined situations. This insightful analysis raises important questions about the limitations of traditional economic models and the need for new approaches to understanding human behavior.

Continuing the discussion, a paper written by W. Brian Arthur in 1994 illustrates the concept of thinking inductively and presents a dynamic problem called “*El Farol Bar.*”  [1] This paper provides further insight into the limitations of traditional economic models and the need for new approaches to understanding human behavior

The problem arises when people decide whether to go to the El Farol bar on a Thursday night to hear Irish music. They would go if they expected few people to be there, but would stay home if they expected it to be crowded. This creates a logical self-contradiction where forecasts that many would attend would lead to few attending, and forecasts that few would attend would lead to many attending.
The problem shows that indeterminacy, heterogeneity, an evolving ecology, and self-organization arise naturally in economic problems. If there were an obvious “rational” model that all agents could use to forecast attendance and base their decisions on, then a deductive solution would be possible. However, this is not the case. Rationality is ill-defined, so the problem of choosing a solution is not well-defined. Agents face fundamental uncertainty: they don’t know how other agents will decide on their forecasts.
By similar reasoning, any commonality of expectations gets broken up and agents will be forced to differ. It is reasonable to assume that agents will update or replace their forecasting methods if they don’t work. The problem immediately becomes adaptive as well as agent-based. Individual forecasts compete to be valid in a situation dependent on others’ forecasts. In other words, forecasts compete in an “ecology” of forecasts.
The ecology of expectations self-organizes into an equilibrium pattern which hovers around the “comfortable” level in the bar. If fewer came in the long term, low forecasts would be valid, so many would come. An attraction to this level emerges. This emergent outcome is organic in nature, for while the population of forecasts on average supports this “comfortable” level, it keeps changing in membership forever. It is something like a forest whose contours do not change, but whose individual trees do.
These properties are robust to changes in types of forecasts created as long as there is a reasonable diversity of them. The El Farol bar problem has since spawned many “solutions,” variants, and further papers. But solutions were not quite Arthur’s intention. At the time, economists had become interested in indeterminacy and fundamental uncertainly, and Arthur was looking to formulate a suitable “toy problem” to illustrate these—a stripped-down problem that’s simple to state but whose outcome or resolution brings a wealth of lessons.

<p align="center">
    <img src="https://github.com/mahdikohan/complexityEconomics/blob/9d1e7f565068ac55eba46e1cc692d2fc63d6f318/El_Farol_Bar/images/fig1.PNG" alt="Dynamic model" width="700">
</p>
<p align="center">Figure 1: El Farol Bar problem simulation.</p>

To solve the El Farol problem, we used a computer engineering method published by the Department of Electrical and Computer Engineering . The problem is posed as shown in Figure 1. The objects used for simulation are illustrated in Figure 1 as follows:

- **Agents**: people who want to go to the bar or stay home
- **Iteration (ticks)**: number of rounds (number of weekends)
- **Memory**: number of recent outcomes
- **Strategy**: decision strategy (defined to simulate randomness in decision and long memory optimizer)

The mechanism by which a person makes a decision is shown in Figure 2.
<p align="center">
    <img src="https://github.com/mahdikohan/complexityEconomics/blob/5beb05ee5fea4fdd3d8d2f061171863a378eb85c/El_Farol_Bar/images/fig2.PNG" alt="Dynamic model" width="600">
</p>
<p align="center">Figure 2: Minority game model of an agent playing the game.</p>

In summary, we can write some equations that are used to simulate the dynamic model:

$$
x = \\frac{-b \\pm \\sqrt{b^2 - 4ac}}{2a}
$$

For more information, you can refer to the main documentation that we used .

## References

[1] Arthur, W. Brian. “Inductive Reasoning and Bounded Rationality.” The American Economic Review 84, no. 2 (1994): 406–11. http://www.jstor.org/stable/2117868.
[2] https://www.ece.rutgers.edu/~marsic/books/SE/projects/MinorityGame/ElFarolBar.pdf
