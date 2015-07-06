# respect matrix
(c) mark p xu neyer
2015
bsd

# Motivation
Suppose Alice respects Bob. If Bob introduces Alice to his friend Claire, and Bob says "this is my good friend Claire", and then Alice is direspectful to Claire, then she is also being disrespectful to Bob. Being respectful to someone means extending your respect to the people _they_ respect.  Respect is _transitive_. Because the entire world is connected, this has some interesting consequences if we start keeping track of who we say we respect, and who we say we don't respect.

The respect matrix is a political mechanism - it provides an incentive for people who are not directly involved with a conflict to help resolve the conflict. 

It works on a very simple principle: freedom of speech. Each person involved in a respect matrix is able to publicly say "I respect this person", or "I do not respect that person".  Matrix algebra allows us to combine all of these statements together, so that you can determine how much implied respect you have for a person you are hiring - say, someone who is going to redo your bathroom. If a good friend of yours says "This contractor did a great job", and you see the bathroom, you are much more likely to trust the contractor than if you get the same recommendation from a total stranger - or from someone you actively distrust.

# Mathematics

Suppose there are N people involved in a social system. A respect matrix for this system is an N x N matrix, with all entries being either -1, 0 or 1.  Each person _i_ is free to put whatever value they want into entry _i,j_ for each other person _j_. If entry _i,j_ is 1, this means person _i_ has stated that they respect person _j_.  If entry _i,j_ is -1, this means person _i_ has stated that they do not respect person _j_ - perhaps because person _j_ has wronged them.  If entry _i,j_ is zero, this means that person _i_ has not publicly stated how they feel about person _j_. 

We actually use two matrices to track statements - one containing only statements of respect (The respect matrix), and another containing only statements of disrespect (The disrespect matrix). This makes the math easier. We also prevent people from making statements about themselves - all entries _i,i_ are always zero. Again, for the sake of mathematics. You are free to respect yourself, and i suggest that you do so, but the math of this system works much better if we ignore those claims in the matrix.

## Transitive Respect

Take a respect matrix and multiply it by itself - this gives you the _implied_ respect of people in the matrix for each other that they don't know direclty, but through a friend. For example in the case above, where Alice respects Bob, and Bob respect claire, the respect matrix is:

  [0, 1, 0]
  [0, 0, 1],
  [0, 0, 0],

The first row has entry _1,2_ being 1, because Alice (person 1) respects Bob (person 2). 
The second row has entry _2,3_ being 1, because Bob (person 2) respects Claire (person 3).
The third row is all 0's - Claire has not made any statements.

When we multiply this matrix by itself, we get the following result:

  [0, 0, 1]
  [0, 0, 0],
  [0, 0, 0],

There is only a single '1' in this matrix - it is in position _1,3_, which means that Alice has 'implied respect' for Claire. 

## Explicit and Implied Respect

The respect matrix consists of statements people have made about who they respect and who they don't - statements people have made, explicitly.  The respect matrix multiplied by itself gives us "implied respect paths of length two" - that is,  the respect people have for one another that is _implied_ by all the statements of everyone in the graph - but only for people 'two hops' away. Alice respects Bob, and Bob respects claire - that's two hops from Alice to Claire. By multiplying the respect matrix by itself, again, we can get implied respect of length 3, and length 4, and so on.

The concept of 'implied respect' allows the respect matrix to help people predict the quality of their interactions with strangers. It can be used to provide implied trust ratings for merchants or service providers, and to help find bad actors who perhaps have not done anything illegal, but have upset a large number of people.

It also has another, more interesting aspect which will be expanded later - it provides a number of people with incentive to resolve social conflicts. It would allow us to determine whose statements we could state seriously, for lack of contradiction. 

### Computing Implied Respect

For the purposes of computation, we can take the respect matrix and break it down into two matrices - P, consisting only of 'respect' statements, and N, consisting only of 'disrespect' statements. To compute the implied matrix, we sum two order 1 terms, two order 2 terms, two order 3 terms, and so on.

For example, consider the three Person system with respect as follows:

     M =  0 1 0
          1 0 1
         -1 1 0

Person 1 respects Person 2 and has no opinion of Person 3.

Person 2 respects both Person 1 and Person 3.

Person 3 does not respect person 1, and respects person 2.


The postive matrix is:

     P =  0 1 0
          1 0 1
          0 1 0

The negative matrix is:

     N =  0 0 0
          0 0 0
         -1 0 0

The order 1 terms are just P and N - thus, the order 1 implied matrix is the same as the explicit matrix.

The order 2 terms are `PxP` and `PxN` - these correspond to length two paths. The matrix `PxP` contains a description of the implied respect due to all length two, strictly postive paths. In our example:

     P x P = 1 0 1
             0 2 0
             1 0 1
           
  Person 1 has no length-2 path to Person 2, and thus has no implied respect for Person 2 in this matrix.  Because Person 1 has respect for Person 2, and Person 2 has respect for Person 3, the matrix P x P says Person P has implied respect for Person 3. Likewise, P x N contains the implied respect of all length two paths which start positive and end negative:

     P x N =  0 0 0
             -1 0 0
              0 0 0
   
Becuase Person 2 respects Person 3, and Person 3 has does not respect Person 1, this means Person 2 has implied respect of  '-1' for person 1. An issue arises here: implied respect doesn't decay over distance. If A respects B, B respects C, C respects D, and D respects E, then without a distance cutoff, A respects E, just as much as a respects B. We'd like to capture the idea that you aren't _always_ bound to respect your the friend of your friends. Therefore we add a 'decay factor' which i've placed somewhat arbitrarily at k = 0.7 This gives the property that someone three hops away has implied respect of  ~ 0.5, instead of 1. The exact number is not super relevant here; the goal is just to discount beliefs of people who are further away from you on the social graph, so that people you are closer to have more weight in terms of who you are likely to respect.

The total Order 2 Implied respect, then, is:

       P + N + (P x P)*k +  (P x N)*k = 
j
      0 1 0   0 0 0   0.7 0   0.7      0   0  0     0.7 1.0 0.7
      1 0 1 + 0 0 0 + 0.0 1.4 0.0  +  -0.7 0  0  =  0.3 1.4 1.0
      0 1 0  -1 0 0   0.7 0   0.7      0   0  0    -0.3 1.0 0.7
      
Order 3 implied respect would consist of the above, plus P x P x P * k^2  and P x P x N x k^2- that is, all length three paths that are strictly postive, and all length three paths that have two positive edges followed by a negative one.

Order 4 respect would consist of Order 3 implied respect, plus P x P x P x P x k^3 and P x P x P x N x k^3 - all length four paths that are either strictly positive, or have exactly one negative edge at the end. 

## Soundness

  One way to look at  row _i_  of a respect matrix is to see it as a vector, in people space, pointing in the direction of the people that person _i_ says they respect. We can interpret row _i_ of the implied respect matrix in the same way - only person _i_ doesn't have direct control over this row; it is a function of _i_'s statements about who _i_ respects, as well as the statemetns of the people _i_ respects, and the people they respect, and so on.  By only adding negative edges at the end of paths, we prevent anyone person _i_ disrespects from having direct influence over the direction of person _i_'s implied respect vector.

We can use the dot product to compare a person's explicit respect vector to their implied respect vector. Let's do that in our example. Here are the explicit and the Order 2 implied respect matricies. We'll normalize this dot product by the magnitude of i's explicit respect vector, to get a measure of how much the implied matrix reflects each person's stated respect:

     M =                     I = 
       0.0 1.0 0.0             0.7 1.0 0.7
       1.0 0.0 1.0             0.3 1.4 1.0
      -1.0 1.0 0.0            -0.3 1.0 0.7


Person 1's explicit respect vector is `[0 1.0 0]`.  Their implied respect vector is `[0.7 1.0 0.7]`. The dot product of these two is 0.0 * 0.7 +  1.0 * 1.0 + 0.0 * 0.7 =  1.0. Dividing this by 1.0, the magnitude of Person 1's explicit vector, we get a total soundness of 1.0

Person 2's explicit respect vector is `[1.0 0.0 1.0]`, and their implied respect vector is `[0.3 1.4 1.0]`. The dot product of these two is 1.3. Dividng by the magnitude of Person 2's explicit vector (sqrt(1+1) = 1.414), we get a total soundness of 0.919.

Person 3's explicit respect vector is `[-1.0 1.0 0.0 ]`, and their implied respect vector is `[-0.3 1.0 0.7]`. The dot product of these two is 0.3. Dividng by the magnitude of Person 3's explicit vector (1.414), we get a total soundness of 0.212.

The person here with the lowest soundness is Person 3 - that is because Person 3 respects Person 2, who respects Person 1, while Person 3 also direspects Person 1.  Person 2 takes a small hit to their soundness, because they respect someone (Person 3) who disrespects someone Person 2 respects (Person 1). If Person 2 wishes to improve their soundness score, they can do any combination of the following:

   * Pick sides, and drop respect for either Person 1 or Person 3.
   * Lower respect for both Person 1 and Person 3
   * Try to work with Person 1 and Person 3 to resolve the dispute.

Suppose, as a result of Person 2's intervention, Person 3 decides to increase their respect for Person 1 - up to 0.0. Person 3 says publicly "I have no opinion of Person 1". They haven't _endorsed_ Person 1 as respectable - they are just saying that they don't disrespect Person 1.

The new implied matrix here is:

      I =  
        0.7 1.0 0.7
        1.0 1.4 1.0
        0.7 1.0 0.7

  Notice that Person 1, who has no opinion of Person 3, remained the same. Person 2 now has more implied respect for Person 1 (up to 1.0 from 0.3), and Person 3 now has implied respect for Person 1. How does this new implied matrix respect soundness?

Person 1 stays the same, as their implied respect vector stayed the same.

Person 2 now has an explicit/implied dot product of 2, for a soundness of 1.414, a gain of 54%.

Person 3 now has an explicit/implied dot product of 1.0, for a soundness of 1.  This is much higher than Person 3's previous soundness of 0.212. If you want to be taken seriously in public, your words have to match up to themselves. The respect matrix allows us to measure, in a very limited sense, the extent to which our professed trust and respect for our peers actually makes sense.
  

Person 2 has improved their social standing (among people who find soundness of explicit and implied respect a worthy goal) by resolving a conflict between two people they know. *A primary goal of the respect matrix is to provide new incentive for people who are not directly involved in a conflict, but know the conflicting parties, to help find a compromise.*

    In short, the respect matrix is a mechanism where multiple parties to a dispute have interest not solely in choosing one side over the other, but in repairing the dispute to increase their standing. It allows for us to identify bad actors who have upset large numbers of people without being charged in court (ahem), and provides us with a strong reason to drop minor disputes and focus on rooting out people who really are causing big problems, and encouraging them to stop and repair the damage they've caused.

  It is impossible for me to imagine a spacefaring civilization, with settlements spanning a galaxy, choosing its leaders in the absurd way we do now, all of us picking between two people we don't really like. I imagine they'd use something like this. And I really, really want to go travel elsewhere in this galaxy. Don't you?
