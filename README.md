# MatchBot
![MatchBot Logo](MatchBotBanner.png)

MatchBot is a Discord-based dating bot. It allows users to create and customize their own profiles, 
shows mutually compatible ones, and notifies both users if they match. This is all done over PMs.
Users need to be added to the allowlist before they can use the bot. This feature was implemented because access to 
the developer-ran instance needed to be restricted to students of Batory High School only.

## Commands

### Profile Setup:

  `!start`                   Shows the intro message

  `!setup`                   Begins account setup

  `!set <element> <content>` Changes parts of your profile

### Profile Tools:

  `!publish`                 Makes your profile viewable to others

  `!unpublish`               Hides your profile

  `!delete-profile`          PERMANENTLY deletes your profile and all associated data

### Profile Browsing:

  `!swipe`                   Shows a random compatible profile

  `!view-profile [user-id]`  Shows either your own profile or a specified user's

### Admin:

  `!allow <user>`            Adds a user to the allowlist

  `!unallow <user>`          Removes a user from the allowlist

  `!allow-all`               Adds all users in the channel to the allowlist

  `!backup`                  Backs up the entire database and allowlist

  `!id <user>`               Returns a user's Discord ID

  `!del-acc <user>`          Deletes a user's account

  `!unallow-all`             Clears the allowlist

  `!create-default-tables`   Adds the default tables to the database

### Info:

  `!info <element>`         Provides information on all the elements of your profile