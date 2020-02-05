## Papers, Please
The concept of this project is derived from the video game, but it is not meant to be a direct representation.

Papers, Please is an indie video game where the player takes on the role of a border crossing immigration officer in the fictional 
dystopian Eastern Bloc-like country of Arstotzka. As the officer, the player must review each immigrant and returning citizen's passports and other supporting paperwork against a list of ever-increasing rules using a number of tools and guides, allowing 
in only those with the proper paperwork, rejecting those without all proper forms, and at times detaining those with falsified information. 

There are a total of 7 countries: Arstotzka, Antegria, Impor, Kolechia, Obristan, Republia, and United Federation. 
### Rules
You have to make an admission decision in according of [сonditions for passing inspection](https://github.com/Sherrbethead/Papers-please/new/master?readme=1#conditions-for-passing-inspection) (default decision is yes). After third mismatching you will be fired (it means game over). 

Also, after the first game day, you will be asked to take a rest and quit from the game (default answer is no).
### Bulletin receiving 
Each morning you are issued an official bulletin from the Ministry of Admission. This bulletin will provide regulations, procedures and the name of a wanted criminal. It may include one or more of the following:
* permanent:
> Entrants require passport

> Foreigners require access permit
* changing:
1. the list of nations (comma-separated if more than one) whose citizens may enter, for example:
> Allow citizens of Obristan, United Federation
2. required vaccinations, for example:
> Citizens of Antegria, Republia, Obristan require polio vaccination
3. currently wanted criminal, for example:
> Wanted by the State: Hubert Popovic
### Inspection
Each day, a number of user-defined entrants (default value is 5) line up outside the checkpoint inspection booth to gain passage into Arstotzka. You will receive an each entrant's set of identifying documents. It will contain zero or more properties which represent separate documents. These properties may include the following:
* passport
* certificate of vaccination
* access permit
* grant of asylum
* diplomatic authorization
### Conditions for passing inspection
1. All required documents are present
2. There is no conflicting information across the provided documents
3. All documents are current (i.e. none have expired) - a document is considered expired if the expiration date is date of playing the game or earlier
4. The entrant is not a wanted criminal
5. If a certificat of vaccination is required and provided, it must list the required vaccination
6. If entrant is a foreigner, a grant of asylum or diplomatic authorization are acceptable in lieu of an access permit. In the case where a diplomatic authorization is used, it must include Arstotzka as one of the list of nations that can be accessed.
7. If the entrant passes inspection, the answer will be one of the following:

    If the entrant is a citizen of Arstotzka: 
    
    > Glory to Arstotzka.
    
    If the entrant is a foreigner: 
    
    > Cause no trouble.
    
8. If the entrant fails the inspection due to expired or missing documents, or their certificate of vaccination does not include the necessary vaccinations, the answer will be "Entry denied" with the reason for denial appended.

    Example 1: 
    
    > Entry denied: passport expired.
    
    Example 2: 
    
    > Entry denied: missing required vaccination.
    
    Example 3: 
    
    > Entry denied: missing required access permit.
    
9. If the entrant fails the inspection due to mismatching information between documents (causing suspicion of forgery) or if they're a wanted criminal, the answer will be "Detainment" with the reason for detainment appended.

    Example 1: 

    >Detainment: ID number mismatch.
    
    Example 2:
    
    > Detainment: Entrant is a wanted criminal.
    
10. In some cases, there may be multiple reasons for denying or detaining an entrant. For this exercise, you will only need to provide one reason.
If the entrant meets the criteria for both entry denial and detainment, priority goes to detaining. For example, if they are missing a required document and are also a wanted criminal, then they should be detained instead of turned away. In the case where the entrant has mismatching information and is a wanted criminal, detain for being a wanted criminal.

### Data examples
* Bulletin
```
Entrants require passport
Allow citizens of Impor, United Federation, Republia, Kolechia
Foreigners require access permit
Citizens of Kolechia, Republia require hepatitis A vaccination
Wanted by the state: Williams, Martha
```
* Entrant 
```
DOCUMENT: passport
ID#: JNE1Y-SWVW4
NATION: United Federation
NAME: Williams, Martha
DOB: 1988.08.06
SEX: F
EXP: 2021.08.08
-----------------
DOCUMENT: certificate of vaccination
NAME: Williams, Martha
DOB: 1988.08.06
VACCINES: hepatitis A, tuberculosis, rubella
-----------------
DOCUMENT: grant of asylum
NAME: Williams, Martha
NATION: United Federation
ID#: JNE1Y-SWVW4
DOB: 1988.08.06
EXP: 2021.07.31
```
