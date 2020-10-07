# Role_Play_Game
a diverting text-based role-play-game written in Python 3.
#### The player can:
- Move through a virtual world
- Interact with the surroundings and follow a storyline by completing tasks
- Get into fights, lose and gain health
- Find, equip, buy and sell items

#### Implementation:
-  Virtual world: Modelled as an undirected graph network with the nodes as world locations.
    More edges are added as the player advances in the story
- Game mechanics: Instances of characters and world locations call each other's class methods, directly - or indirectly via lambda functions  

#### +++ To Do: Code Cleanup - Refactoring, splitting code into more files, set up a "main"-file, improve overall readability

## Content of the repository

1. __Python Code__: the folder `Python Code` contains the following script files:
    * __world_map.py__:  
            - game mechanics  
            - contains the main code which imports the files `characters.py` and `items.py` and instantiates their classes  
            - contains the graph network of  the game world and the classes of associated world locations  
            - contains asscociated helper functions  
          
    * __characters.py__:  
            - contains the `Character`-superclass and the derived hero-class and opponent-classes  
            - contains associated helper methods  
    * __items.py__:  
            - contains classes of items whose instances can be 'used' by the hero class  
           

2. __Compiled Game__: the folder `Compiled Game` contains the files after compilation using `pyinstaller` in the `Bash`-shell:
    * __world_map.exe__:  
            - execute this file to run the compiled game  
    * additional files:  
            - misc. files created during compilation  
           

3. __Screenshots__: the folder `Screenshots` contains some representative pictures of the gameplay (format = .png)
            
        
***


Contact m.bachmaier@posteo.de for further information.  
