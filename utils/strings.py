from utils import config


class Help:
    set_name = 'To set your name, use the command\n' \
               '```!set name <full name>```\n' \
               'With `<full name>` being the name you wish to use. ' \
               'Maximum characters: 50\n\n' \
               '**Examples:**\n' \
               '```!set name Jan Kowalski```\n' \
               '```!set name Jan K.```\n' \
               '```!set name X Æ A-12```\n'

    set_class = 'To set your class, use the command\n' \
                '```!set class <class name>```\n' \
                'With `<class name>` being the shortened name of the class you are currently in. ' \
                'Maximum characters: 6\n\n' \
                '**Examples:**\n' \
                '```!set class 2ibA```\n' \
                '```!set class 1C```\n' \
                '```!set class 2niA```\n'

    set_age = 'To set your age, use the command\n' \
              '```!set age <age>```\n' \
              'With `<age>` being a number between 15 and 19.\n\n' \
              '**Examples:**\n' \
              '```!set age 15```\n' \
              '```!set age 17```\n' \
              '```!set age 19```\n'

    set_gender = 'To set your gender, use the command\n' \
                 '```!set gender <M(ale)/F(emale)/O(ther)> [custom gender name]```\n' \
                 'You can currently choose one of 3 primary genders: `Male`, `Female`, and `Other`. ' \
                 'They also go by the shortcuts `M`, `F`, and `O`. \n' \
                 '`[custom gender name]` is optional, and lets you input your own gender to be displayed ' \
                 'alongside your primary gender. In most cases, that will be `Other`. ' \
                 'Custom genders can have up to 25 characters. \n\n' \
                 '**Examples:**\n' \
                 '```!set gender Male```\n' \
                 '```!set gender F```\n' \
                 '```!set gender Other Non-binary```\n'

    set_preference = 'To set which genders you\'d like to see when going through profiles, use the command\n' \
                     '```!set preference <MFO>```\n' \
                     'You can select any combination of `Male`, `Female`, and `Other` you\'re into.\n\n' \
                     '**Examples:**\n' \
                     '```!set preference M```\n ^ You\'ll only see `Male` profiles\n' \
                     '```!set preference FO```\n ^ You\'ll see both `Female` and `Other` profiles\n' \
                     '```!set preference MFO```\n ^ You\'ll see profiles from all available genders'

    set_bio = 'To set your bio, use the command\n' \
              '```!set bio <bio>```\n' \
              'With `<bio>` being a longer piece of text you\'d like everyone to see on your profile. ' \
              '(Tip: Use Shift+Enter on desktop or the Enter key on mobile to add a new line) ' \
              'Maximum characters: 500\n\n' \
              '**Examples:**\n' \
              '```!set bio Hey there! I like hiking, Netflix, and making really bad decisions.```\n' \
              '```!set bio\n' \
              'ENTP||5\'6"||🍕🍨🍔\n' \
              'My mom thinks I\'m cool.```\n' \
              '```!set bio\n' \
              'Hejka~ 😉```'

    set_pic = 'To set your profile picture, simply send a photo, and it\'ll replace your current one automatically. ' \
              'We recommend using a high quality image, 720p at a minimum.\n\n' \
              'Supported file types: `.png`, `.jpg`, `.jpeg`\n' \
              'Maximum file size: `8 Megabytes`'


class ProfileSetup:
    start_message = 'MatchBot is Batory\'s very own dating bot!\n' \
                    'Before you can `!swipe` away to your heart\'s content, you first need to create a profile.\n' \
                    'We\'d also like you to abide by a couple of rules:\n\n' \
                    '**Rules:**\n' \
                    '1. No harassment, hate speech, illegal content, etc.\n' \
                    '2. Don\'t impersonate other students - use your real name.\n' \
                    f'3. Only `like` profiles you\'re *actually* into - don\'t just hit {config.yes_emoji} ' \
                    'on everyone you see.\n\n' \
                    '**Setup:**\n' \
                    'Assuming you\'ve already been verified, use the `!setup` command to create a profile. ' \
                    'It\'ll tell you exactly what to do, and offer helpful instructions along the way! ' \
                    'You can edit any part of your profile after you finish. ' \
                    'Try it now:\n' \
                    '```!setup```'

    not_on_allowlist = 'Sorry, ' \
                       'you\'re not currently on our list of Batory students. ' \
                       'MatchBot is Batory-exclusive, and only users on our ' \
                       'allowlist can create a profile. ' \
                       'If you are a student and haven\'t yet been added, please ' \
                       'contact the developer or wait until we update the list.'

    edit_profile = 'You already have a profile, but you can still edit any part of it at any time. ' \
                   'Just keep in mind that any changes won\' apply to versions of your profile already ' \
                   'sent to someone else, only new `!swipe`s. ' \
                   'To edit your profile, use the following commands:'

    ready_to_publish = 'You\'re all done! ' \
                       'Your profile is now ready to be added to the database and shown to other users. ' \
                       'If you\'d like to see how your profile looks first, run `!view-profile`. ' \
                       'To begin using MatchBot for real, use the command `!publish` to complete profile setup.\n\n' \
                       'Try it now:\n' \
                       '```!view-profile```\n' \
                       '```!publish```'

    published_message = 'You can now start viewing other people\'s profiles! \n' \
                        'To begin, use the command `!swipe`. It\'ll show you a random compatible profile ' \
                        f'that you can then react to with a {config.yes_emoji} or {config.no_emoji}. ' \
                        f'You can change your reaction at any time, and we\'ll remember your new choice. \n' \
                        f'After you add a reaction, the bot will show you the next profile in your queue ' \
                        f'and will continue showing you more profiles automatically. \n\n' \
                        'Try it now:\n' \
                        '```!swipe```'


class Swipe:
    no_compatible_profiles = 'Sorry, we couldn\'t find any more compatible profiles ' \
                             'based on your gender and preferences. ' \
                             'We only show you profiles whose gender is included in your preferences, ' \
                             'and whose own preferences include your gender. \n' \
                             'There are currently `{user_count}` profiles in our database. ' \
                             'If that number seems low, check back in a bit. New users join all the time! \n' \
                             'You can also change your settings to expand your profile pool, then `!swipe` again. ' \
                             'To see how to change your gender preferences, use `!info preferences`. '

    mutual_match = 'Congratulations! You and {user_name} ({user_mention}) just matched with each other! ' \
                   'This means they liked your profile too, so go ahead and message them.\nGood luck! 💖'
