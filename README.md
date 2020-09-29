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
- Game mechanics: Instances of characters and world locations call each others class methods, directly or indirectly via lambda functions  



## Content of the repository

1. __Python Script__: the folder `Python Script` contains the following script files:
    * 'world_map.py':  
            - game mechanics  
            - contains the main code which imports the files 'characters.py' and 'items.py'  
            - contains the graph network of  the game world and the classes of associated world locations
            - contains asscociated helper functions  
          
    * 'characters.py':  
            - contains the 'Character'-superclass and the derived hero-class and opponent-classes  
            - contains associated helper methods  
    * 'items.py':  
            - contains classes of items whose instances can be 'used' by the hero class  
           

2. __Compiled Game__: the folder `Compiled Game` contains the files after compilation using 'pyinstaller' in the 'Bash'-shell:
    * 'world_map.exe':  
            - execute this file to run the compiled gamethods  
    * additional files: 
            - misc. files created during compilation  
            
        
***


Contact m.bachmaier@posteo.de for further information.  
