# respect matrix
(c) mark p xu neyer
2015
bsd



# A Reputation System
## Not "Yelp for People."  More like "OK Cupid,  for any interaction, not just dating"

The respect matrix is a reputation system.  

Most reputation systems give people or businesses ratings. Yelp rates businesses. Uber gives ratings for drivers and riders, and  AirBnb gives ratings for guests and hosts.  The are problem with ratings: they can be gamed, they can be widly unfair, and it's hard to answer what "rating a person" would even mean.

The respect matrix is different. It works more like a dating website. Instead of giving each person an 'absolute score' to say how good of a partner they are, most dating websites give something like a *match score*.     A "match score" is meant to be an estimate of how much *you* would like a given person.   Someone else looking at the same person would get a different match score.

A "match score" only has meaning when talking about two people. You can't go on OKCupid and see 'how good you are'.  You can, however, see how good a given person might be as a partner for you.  That is how the respect matrix works: there is no score for you that you or anyone else can see. It's not "hidden"; it simply doesn't exist. You *can* see *personalized* scores for other people, which tell you how confident the respect matrix is that you will have a positive interaction with those other people. 

You can't ask the respect matrix "What is my score?", because the respect matrix doesn't work that way.  You don't *have* a score.

You *can* ask it, "Should I do business with / rent my house to / go on a trip with / talk politics with  this person?"

You can also ask it, "Who are some people who you think will like me? Who are you some people who you think won't like me?"

You can also ask it, "I have a conflict with Bob. Who are some people who respect both Bob and myself, who might help resolve this dispute?"

# Friends of Friends of Friends ...
## When your friends introduce someone they respect, you're more likely to respect them.

You use the respect matrix by just telling it people you respect, and people you don't respect. It can also work with companies or organizations - they're all the same to the respect matrix.  You can tell the matrix that you 'respect' or 'disrespect' any entity.  These statements are like vouching for someone. You can either vouch _for_ someone, or you vouch against them.

![](http://i.imgur.com/o33KYKP.png)

In this example, each blue line  represents a 'respect' statement. The red lines represent a 'disrespect' statement. 

The total confidence that the respect matrix has about my interaction with that possible roommate would be the sum of all of those paths.

There are now two working implementations: [one on facebook](https://www.facebook.com/respectmatrix), and [another on twitter](https://twitter.com/RespectMatrix). The facebook implementation uses the 'drops' app for django which is in the enclosed directory. The twitter one is based on the same code.


# How it Works
Suppose Alice respects Bob. If Bob introduces Alice to his friend Claire, and Bob says "this is my good friend Claire", and afterwards Alice is disrespectful to Claire, then she is also being disrespectful to Bob. Being respectful to someone means extending your respect to the people _they_ respect.  Respect is _transitive_. Because the entire world is connected, this has some interesting consequences if we start keeping track of who we say we respect, and who we say we don't respect.

The respect matrix is a political mechanism - it provides an incentive for people who are not directly involved with a conflict to help resolve the conflict. 

It works on a very simple principle: freedom of speech. Each person involved in a respect matrix is able to publicly say "I respect this person" or "I do not respect that person".  Matrix algebra allows us to combine all of these statements together, so that you can determine how much implied respect you have for a person you are hiring - say, someone who is going to redo your bathroom. If a good friend of yours says "This contractor did a great job", you are much more likely to trust the contractor than if you get the same recommendation from a total stranger - or from someone you actively distrust.

# Mathematics

Suppose there are N people involved in a social system. A respect matrix for this system is an N x N matrix, with all entries being either -1, 0 or 1.  Each person _i_ is free to put whatever value they want into entry _i,j_ for each other person _j_. If entry _i,j_ is 1, this means person _i_ has stated that they respect person _j_.  If entry _i,j_ is -1, this means person _i_ has stated that they do not respect person _j_ - perhaps because person _j_ has wronged them.  If entry _i,j_ is zero, this means that person _i_ has not publicly stated how they feel about person _j_. 

We actually use two matrices to track statements - one containing only statements of respect (The respect matrix), and another containing only statements of disrespect (The disrespect matrix). This makes the math easier. We also prevent people from making statements about themselves - all entries _i,i_ are always zero. Again, for the sake of mathematics. You are free to respect yourself, and I suggest that you do so, but the math of this system works much better if we ignore those claims in the matrix.

## Transitive Respect

Take a respect matrix and multiply it by itself - this gives you the _implied_ respect of people in the matrix for each other that they don't know direclty, but through a friend. For example in the case above, where Alice respects Bob, and Bob respects Claire, the respect matrix is:

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

It also two more interesting aspects which will be expanded later - it provides a number of people with incentive to resolve social conflicts, and it would allow us to determine whose statements we could take seriously, for lack of contradiction. 

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
   
Becuase Person 2 respects Person 3, and Person 3 has does not respect Person 1, this means Person 2 has implied respect of  '-1' for person 1. An issue arises here: implied respect doesn't decay over distance. If A respects B, B respects C, C respects D, and D respects E, then without a distance cutoff, A respects E, just as much as a respects B. We'd like to capture the idea that you aren't _always_ bound to respect your the friend of your friends. Therefore we add a 'decay factor' which i've placed somewhat arbitrarily at k = 1/8 = 0.125. The exact number is not super relevant here; the goal is just to discount beliefs of people who are further away from you on the social graph, so that people you are closer to have more weight in terms of who you are likely to respect.

The total Order 2 Implied respect, then, is:

       P + N + (P x P)*k +  (P x N)*k = 
       
       0 1 0   0 0 0   0.125 0    0.125      0     0  0     0.125 1    0.125
       1 0 1 + 0 0 0 + 0.0   0.25 0.0    +  -0.125 0  0  =  0.875 0.25 1
       0 1 0  -1 0 0   0.125 0    0.125      0     0  0    -0.875 1    0.125
       
Order 3 implied respect would consist of the above, plus P x P x P * k^2  and P x P x N x k^2- that is, all length three paths that are strictly postive, and all length three paths that have two positive edges followed by a negative one.

Order 4 respect would consist of Order 3 implied respect, plus P x P x P x P x k^3 and P x P x P x N x k^3 - all length four paths that are either strictly positive, or have exactly one negative edge at the end. 

## Soundness

  One way to look at  row _i_  of a respect matrix is to see it as a vector, in people space, pointing in the direction of the people that person _i_ says they respect. We can interpret row _i_ of the implied respect matrix in the same way - only person _i_ doesn't have direct control over this row; it is a function of _i_'s statements about who _i_ respects, as well as the statements of the people _i_ respects, and the people they respect, and so on.  By only adding negative edges at the end of paths, we prevent anyone person _i_ disrespects from having direct influence over the direction of person _i_'s implied respect vector.

We can use the dot product to compare a person's explicit respect vector to their implied respect vector. Let's do that in our example. Here are the explicit and the Order 2 implied respect matricies. We'll normalize this dot product by the sum of the 1's of i's explicit respect vector, to get a measure of how much the implied matrix reflects each person's stated respect:

     M =                     I = 
       0.0 1.0 0.0             0.125 1.0  0.125
       1.0 0.0 1.0             0.875 0.25 1.0
      -1.0 1.0 0.0            -0.875 1.0  0.125


Person 1's explicit respect vector is `[0 1.0 0]`.  Their implied respect vector is `[0.125 1.0 0.125]`. The dot product of these two is 0.0 * 0.125 +  1.0 * 1.0 + 0.0 * 0.125 =  1.0. Dividing this by 1.0, the magnitude of Person 1's explicit vector, we get a total soundness of 1.0. Person 1 has a good soundness score here, because their implied vector points in the same direction as their explicit vector.  In other words, Person 1 has a 'coherent opinion' about where, in people space, respectable people are.

Person 2's explicit respect vector is `[1.0 0.0 1.0]`, and their implied respect vector is `[0.875 0.25 1.0]`. The dot product of these two is 1.875. Dividng by the number of 1's in  Person 2's explicit vector (2), we get a total soundness of 0.9385. Person 2 has a slightly lower soundness score than persone 1. This because Person 2 says that they respect Person 1,  but also Person 3, who doesn't respect person 1. That means Person 2 has a 'slightly contradictory' opinion of Person 1.  Person 2's opinoin about 'where respectable people are' is slightly less coherent, because they respect two people, one of whom disrespects the other. 

Person 3's explicit respect vector is `[-1.0 1.0 0.0 ]`, and their implied respect vector is `[-0.875 1.0 0.125]`. The dot product of these two is 1.0. Dividng by the number of 1's in Person 3's explicit vector (2), we get a total soundness of 0.5.

The person here with the lowest soundness is Person 3 - that is because Person 3 respects Person 2, who respects Person 1, while Person 3 also direspects Person 1.  Person 3's opinion is the 'least coherent', because they don't respect someone that their friend does respect.

If Person 2 wishes to improve their soundness score, they can do any combination of the following:

   * Pick sides, and drop respect for either Person 1 or Person 3.
   * Lower respect for both Person 1 and Person 3
   * Try to work with Person 1 and Person 3 to resolve the dispute.

Suppose, as a result of Person 2's intervention, Person 3 decides to increase their respect for Person 1 - up to 0.0. Person 3 says publicly "I have no opinion of Person 1". They haven't _endorsed_ Person 1 as respectable - they are just saying that they don't disrespect Person 1.

The new implied matrix here is:

      I =  
        0.125 1.0  0.125
        1.0   0.25 1.0
        0.125 1.0  0.125

Notice that Person 1, who has no opinion of Person 3, remained the same. Person 2 now has more implied respect for Person 1 (up to 1.0 from 0.875), and Person 3 now has implied respect for Person 1. How does this new implied matrix respect soundness?

Person 1 stays the same, as their implied respect vector stayed the same.

Person 2 now has an explicit/implied dot product of 2, for a soundness of 1, a gain of 6%.

Person 3 now has an explicit/implied dot product of 1.0, for a soundness of 1.  This is much higher than Person 3's previous soundness of 0.5, because Person 3's opinoin is now more internally consistent.

If you want to be taken seriously in public, your words have to match up to themselves. The respect matrix allows us to measure, in a very limited sense, the extent to which our professed trust and respect for our peers actually makes sense. It also provides an incentive for people who are not directly part of a conflict, to help resolve that conflict.
  

Person 2 has improved their consistency (and thus their social standing) by resolving a conflict between two people they know. *A primary goal of the respect matrix is to provide new incentive for people who are not directly involved in a conflict, but know the conflicting parties, to help find a compromise.*

In short, the respect matrix is a mechanism where multiple parties to a dispute have interest not solely in choosing one side over the other, but in repairing the dispute to increase their standing. It allows for us to identify bad actors who have upset large numbers of people without being charged in court (ahem), and provides us with a strong reason to drop minor disputes and focus on rooting out people who really are causing big problems, and encouraging them to stop and repair the damage they've caused.

It is impossible for me to imagine a spacefaring civilization, with settlements spanning a galaxy, choosing its leaders in the absurd way we do now, all of us picking between two people we don't really like. I imagine they'd use something like this. And I really, really want to go travel elsewhere in this galaxy. Don't you?
