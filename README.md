# respect matrix
(c) mark p xu neyer
2015
bsd

# basics

Define a respect matrix as follows: Entry `M[i,j]` is a real number in `[-1,1]` representing how much Person `i` respects Person `j`.

For example, we can interpret the identity matrix as a respect matrix: The interpretation is that everyone is respects themselves absolutley, and has no opinion of everyone else. 

The 'respect matrix' is like a social game that lets people know who we might enjoy interacting with. Each Person `i` can add whatever value they want, to entry `i,j` specifying how much they respect Person `j`. 1 means total respect , -1 means absolute disrespect.  

## Explicit and Implied Respect

If I bring a friend over, and you are rude to this friend, then you are also being rude to me. The basic idea here is that respect is transitive; if you respect someone, you have to be respectful to anyone they respect.

The raw matrix, consisting essentially of statements people have made, tells us how much people directly say they respect one another.  We can use the raw matrix, which describes 'explicit respect', to compute the 'implied respect' that people should have for others, based upon the statements everyone has made.

The reason respect values are in the range [-1,1], is so that you can multiply values of consecutive relationships together. For example, if Alice's respect for Bob is 0.4, and Bob's respect for Carol is 0.6, then Alice has 'implied respect' for Carol of 0.4 x 0.6 = 0.24.

The implied respect allows the respect matrix to help people predict the quality of their interactions with strangers. It could be used to provide implied trust ratings for merchants or service providers, and to help find bad actors who perhaps have not done anything illegal, but have upset a large number of people.

It also has another, more interesting aspect which will be expanded later - it provides a number of people with incentive to resolve social conflicts. It would allow us to determine whose statements we could state seriously, for lack of contradiction. 

### Computing Implied Respect

For the purposes of computation, we can take the explicit matrix and break it down into two matrices - P, consisting only of positive values, and N, consiting only of negative values. To compute the implied matrix, we sum two order 1 terms, two order 2 terms, two order 3 terms, and so on.

For example, consider the three Person system with respect as follows:

     M =  0.0 0.3 0.0
          0.2 0.0 0.2
         -0.3 0.2 0.0

Person 1 has 0.3 respect for Person 2 and no opinion of  Person 3.
Person 2 has 0.2 respect for Person 1 and 0.2 respect for Person 3.
Person 3 has -0.3 respect for Person 1 and 0.2 respect for Person 2.


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
   
  Person 1 has no length-2 path to Person 2, and thus has no implied respect for Person 2 in this matrix.  Because Person 1 has 0.3 respect for Person 2, and Person 2 has 0.2 respect for Person 3, the matrix P * P says Person P has 0.3 * 0.2 = 0.6 implied respect for Person 3. Likewise, P * N contains the implied respect of all length two paths which start positive and end negative:

     P * N = 
           0.0  0.0  0.0
         -0.06  0.0  0.0
           0.0  0.0  0.0
   
Becuase Person 2 has 0.2 respect for Person 3, and Person 3 has -0.3 respect for Person 1, this means Person 2 has implied respect of  0.2 * -0.3 = -0.06 for Person  1.

The total Order 2 Implied respect, then, is:

       (P + N) + (P * P) +  (P * N) = 

        0.0 0.3 0.0     0.06 0.0  0.06      0.0  0.0  0.0     0.06 0.3 0.06
        0.2 0.0 0.2  +  0.0  0.1  0.0   +  -0.06 0.0  0.0 =   0.14 0.1 0.2
       -0.3 0.2 0.0     0.04 0.0  0.04      0.0  0.0  0.0    -0.26 0.2 0.04

Order 3 implied respect would consist of the above, plus P * P * P and P * P * N - that is, all length three paths that are strictly postive, and all length three paths that have two positive edges followed by a negative one.

Order 4 respect would consist of Order 3 implied respect, plus P * P * P * P and P * P * P * N - all length four paths that are either strictly positive, or have exactly one negative edge at the end. Because the respect values are less than one, the higher order implied respect matrices gradually contribute less and less to the total. This makes sense, because a recomendation from a fiend carries far more weight than a recommendation from a friend of a friend of a friend.


## Soundness

  One way to look at  row _i_  of a respect matrix is to see it as a vector, in people space, pointing in the direction of the people that person _i_ says they respect. We can interpret row _i_ of the implied respect matrix in the same way - only person i doesn't have direct control over this row; it is a function of _i_'s statements about who _i_ respects, as well as  the statemetns of the people _i_ respects, and the people they respect, and so on.  By only adding negative edges at the end of paths, we prevent anyone person _i_ redirespects from having direct influence over the direction of person _i_'s implied respect vector.

We can use the dot product to compare a person's explicit respect vector to their implied respect vector. Let's do that in our example. Here are the explicit and the Order 2 implied respect matricies. We'll normalize this dot product by the magnitude of i's explicit respect vector, to get a measure of how much the implied matrix reflects i's 

     M =                     I = 
       0.0 0.3 0.0             0.06 0.3 0.06
       0.2 0.0 0.2             0.14 0.1 0.2
      -0.3 0.2 0.0            -0.26 0.2 0.04


Person 1's explicit respect vector is `[0 0.3 0]`.  Their implied respect vector is `[0.06 0.3 0.06]`. The dot product of these two is 0.0 * 0.06 +  0.3 * 0.3 + 0.0 * 0.06   =  0.09. Dividing this by 0.3, the magnitude of Person 1's explicit vector, we get a total soundness of 0.3

Person 2's explicit respect vector is `[0.2 0.0 0.2]`, and their implied respect vector is `[0.14 0.1 0.2]`. The dot product of these two is 0.068. Dividng by the magnitude of Person 2's explicit vector (0.283), we get a total soundness of 0.240

Person 3's explicit respect vector is `[-0.3 0.2 0. ]`, and their implied respect vector is `[-0.26 0.2 0.04]`. The dot product of these two is 0.118. Dividng by the magnitude of Person 3's explicit vector (0.361), we get a total soundness of 0.327.

The person here with the lowest soundness is Person 2 - that is because person 2 respects someone (Person 3), who disrespects Person 1, someone respected by Person 2.  If Preson 2 wishes to improve their soundness score, they can do any combination of the following:

   * Pick sides, and drop respect for either Person 1 or Person 3.
   * Lower respect for both Person 1 and Person 3
   * Try to work with Person 1 and Person 3 to resolve the dispute.

Suppose, as a result of Person 2's intervention, Person 3 decides to increase their respect for Person 1, up to -0.05. This is a much weaker statement of disrespect. Let's see how that changes the order 2 implied respect matrix:

      I =  
        0.06 0.3 0.06
        0.19 0.1 0.2
       -0.01 0.2 0.04

  Notice that Person 1, who has no opinion of Person 3, remained the same. Person 2 now has more implied respect for Person 1, and Person 3's implied disrespect is much lower. How does this change soundness?

  Person 1 says the same, as their implied respect vector stayed the same.

  Person 2 now has an explicit/implied dot product of 0.078, for a soundness of 0.426, a gain of 75%. Person 2 has improved their social standing (among people who find soundness of explicit and implied respect a worthy goal) by resolving a conflict between two of their friends.

  Person 3 now has an explicit/implied dot product of 0.0405, for a soundness of 0.197, a loss of 40%.  Why did Person 3's soundness go down? The negative respect for Person 1 is so low that it's outweighed by Person 3's respect for Person 2. It's almost like - hey, this tiny stuff doesn't matter. You holding a grudge against my friend annoys me more than it hurts him, so why don't you just drop it?  Let's suppose Person 3, desirous of being seen as having sound respect, then decides to let bygones be bygones and drops the disrespect for Person 1 from the matrix. The implied respect is now:

      I =  
        0.06 0.3 0.06
        0.2 0.1 0.2
        0.04 0.2 0.04

  And a quick inspection shows that everyone in this list situatino has perfectly sound respect vectors.

  In short, the respect matrix allows for a mechanism where multiple parties to a dispute have interest not solely in choosing one side over the other, but in repairing the dispute to increase their standing. It allows for us to identify bad actors who have upset large numbers of people without being charged in court (ahem), and provides us with a strong reason to drop minor disputes and focus on rooting out people who really are causing big problems, and encouraging them to stop and repair the damage they've caused.

  It is impossible for me to imagine a spacefaring civilization, with settlements spanning a galaxy, choosing its leaders in the absurd way they do. I imagine they'd use something like this. And I really, really want to go travel elsewhere in this galaxy. Don't you?



