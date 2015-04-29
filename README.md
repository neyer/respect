# respect matrix
(c) mark p xu neyer
2015
bsd

# basics

Define a respect matrix as follows: Entry `M[i,j]` is a real number in `[-1,1]` representing how much person `i` respects person `j`.

For example, we can interpret the identity matrix as an identity matrix. The interpretation is that everyone is respects themselves absolutley, and has no opinion of everyone else. 

The 'respect matrix' is like a social game that lets people know who we might enjoy interacting with. Each person `i` can add whatever value they want, to entry `i,j` specifying how much they respect person `j`. 1 means total respect , -1 means absolute disrespect.  

## Explicit and Implied Respect

If I bring a friend over, and you are rude to this friend, then you are also being rude to me. The basic idea here is that respect is transitive; if you respect someone, you have to be respectful to anyone they respect.

The raw matrix, consisting essentially of statements people have made, tells us how much people directly say they respect one another.  We can use the raw matrix, which describes 'explicit respect', to compute the 'implicit respect' that people should have for others, based upon the statements everyone has made.

The reason respect values are in the range [-1,1], is so that you can multiply values of consecutive relationships together. For example, if Alice's respect for Bob is 0.4, and Bob's respect for Carol is 0.6, then Alice has 'implied respect' for Carol of 0.4 x 0.6 = 0.24.

The implied respect allows the respect matrix to help people predict the quality of their interactions with strangers. It could be used to provide implied trust ratings for merchants or service providers, and to help find bad actors who perhaps have not done anythign illegal, but have upset a large number of people.

It also has another, more interesting aspect which will be expanded later - it provides a number of people with incentive to resolve social conflicts.

### Computing Implied Respect

For the purposes of computation, we can take the explicit matrix and break it down into two matrices - P, consisting only of positive values, and N, consiting only of negative values. To compute the implied matrix, we sum two order 1 terms, two order 2 terms, two order 3 terms, and so on.

For example, consider the three person system with respect as follows:

   M =  0.0 0.3 0.0
        0.2 0.0 0.2
       -0.3 0.2 0.0

Person 1 has 0.3 respect for person 2 and no opinion of  person 3.
Person 2 has 0.2 respect for person 1 and 0.2 respect for person 3.
Person 3 has -0.3 respect for person 1 and 0.2 respect for person 2.


The postive matrix is:

   P =  0.0 0.3 0.0
        0.2 0.0 0.2
        0.0 0.2 0.0

The negative matrix is:

   N =  0.0 0.0 0.0
        0.0 0.0 0.0
       -0.3 0.0 0.0

The order 1 terms are just P and N - thus, the order 1 implied matrix is the same as the explicit matrix.

The order 2 terms are `PxP` and `PxN` - these correspond to length two paths. The matrix `PxP` contains a description of the implied respect due to all length two, strictly postive paths. In our example:

  P * P = 
        0.06 0.0  0.06
        0.0  0.1  0.0 
        0.04 0.0  0.04

  Person 1 has no length-2 path to person 2, and thus has no implied respect for person 2 in this matrix.  Because person 1 has 0.3 respect for person 2, and person 2 has 0.2 respect for person 3, then matrix P * P says person P has 0.3 * 0.2 = 0.6 implied respect for person 3.
  N * P = 
        0.0  0.0  0.0
        0.0  0.0  0.0
        0.0  -0.09  0.0



