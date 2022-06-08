## Discord Script
- Utilized: ```PostGreSQL, Heroku, Discord API, Python, JSON, SQLite3```
 

Functionality:
> 1. **React** to giveaways and **notify** the user
> 2. **Won't react** if certain keywords(*eg: fake giveaways*) are in the title of the giveaway 
> 3. **Scan for keywords** mentioned in the specific channel for potential fake giveaways after joining and **alert user to unreact**
> 4. **Exclude certain servers or channels** to join giveaways from 
> 5. **Each notification provide option to unreact** to specific giveaways easily
> 6. **Add**, **remove** and **fetch** *"keywords"/"server to exclude"/"channel to exclude"/"server to leave"* from a database
> 7. **Running** it **24/7** on Heroku
> 8. **Leave multiple servers** with "!leave" command
