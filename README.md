# Human Brain Project (HBP)

## General
This repository contains three separate exhibits for the HBP exhibition + translation scripts for another project, that does not need any software development.
We will briefly descrbie each exhibit and the project, then provide more details about each one in relevant sections below.

### Opening

The opening exhibits is a big touch screen that provides language change support, and various buttons.
The buttons show images, and a rotating caption to understand where each image leads to.
Most buttons show a video (most of them do) and allows to go back to the main screen before the video ends.
One button shows a map, showing all countries in the HBP project, and then for each country, which universities and cities are part of the HBP project, allowing navigation between them.
Finally, there is a credit button that shows credit texts.

### Doctor for a Moment

This exhibit allows the user to conduct three tests on a pateint, and estimate if they have Alzheimer's.
The tests are a combination of either showing a video, or activating a physical model via serial port.
Each time the exhibit runs, the patient either has Alzheimer's or not. Following the estimation, the exhibit explains if it was correct or incorrect.

### Neuron under Construction

This exhibit allows to finger trace some of the neuron paths, out of three possible neuron types.
Then, a 3D model of the neuron is shown, and by a button click you can electrify it.

### Brain Atlas

This exhibit runs a pre-made software received from a 3rd party that shows the parts of the brains.
However, to translate it, we needed to provide with a specific formatted json and all translations.
For this task, a few python scripts were created.
The process is fully detailed at the corrsponding section below.

## Installation & Run
The exhibit runs using python 3 on linux, using the pygame engine and a few other libraries.

After the latest python 3 installation, use:

```
pip install pygame
pip install opencv-python
pip install pyfribidi
pip install pyserial
pip install psutil
pip install evdev
pip install numpy
```

To install all necessary packages (for all exhibits).

Then, to run, go to the root project dir and run the script relevant out of these three options:

```
python3 Opening.py # For opening screen
python3 Neuron.py # For neuron under construction
python3 Doctor.py # For doctor for a moment
```

You can also use the --mouse parameter to run all exhibits with mouse support and not touch (see config for details):

```
python3 Opening.py --mouse
python3 Neuron.py --mouse
python3 Doctor.py --mouse
```

For running the translation scripts for brain atlas, see designated section below.

## Config
All exhibit share a common config file that supporst a vast array of configurations.
In addition, each exhibit has a small additional config file that provides some override configurations.
We will go over each one here, strating with the common config firs, then all override specific config files will follow.

### Common
The common config file is located in assets/config/config.json
Following is a complete description of all options:

#### screenWidth, screenHeight

Specifies the width and height in pixels of the screen (so that full screen will be configured correctly).

#### touch, touchDeviceName, touchMaxX, touchMaxY

These 4 keys define the characteristics of the touch screen connected to the exhibit.
touch should be set to true for the exhibit to use touch (otherwise a mouse is supported).
touchDeviceName is a partial name that is used to match the touch screen device. Use a partial name that is also unique.
You can enumerate all linux devices using this command:

```
lsinput
```

Finally, the touchMaxX and touchMaxY represent the logical screen resolution that evdev works with.
The exhibit will convert these coordinates to the actual screen resolution coordinates.
These usually change with the screen size, and are usually 4096x4096 but can also be 2048x2048 and 1024x1024, or other numbers potentially.
The best way to find out the proper value, is to add print statements in the TouchScreen.py file, in the readTouch method, in case the event type is ecodes.EV_ABS.

Like this:
```
elif event.type == ecodes.EV_ABS:
    absEvent = categorize(event)

    if absEvent.event.code == 0:
        currX = absEvent.event.value
    elif absEvent.event.code == 1:
        currY = absEvent.event.value

    print(currx, curry)
```

Then, run the exhibit, and touch various corners of the screen. It will be very easy to conclude on the max value sknowing they are a power of 2.

#### defaultLanguage

Specifies the default language loaded on startup (he/en/ar).
Note that the prefix to put here should be identical to the prefix defined in the language array (see details below).

#### maxMapDotTapDistance

In the opening exhibit, on the map, this parmaeter defines the maximum distance in pixels that a tap selects a dot on a country map,
so that even if you tap a bit far from the dot, it will still get selected.

#### shouldOpenSerial

Specifies weather the serial port is used in this exhibit and should be opened (only doctor for a moment uses a serial port).

#### PETSerialCommands, MRISerialCommands, PETDoneSerialCommands, initSerialCommands, PETRunTime, MRIRunTime

These are all keys that specify which serial commands should be activated on PET and MRI tests in the Doctor for a Moment exhibit.
Let's describe each one.

The PetSerialCommands and MRISerialCommands keys lead to a serials of time passed in seconds to string command arrays.
The key specifies how many seconds should pass before the commands in the array should be sent to the serial port.

So, for example, in this configuration:

```
{
    "0": ["D 1"],
    "1": ["B -3600 400"],
    "14": ["D 0"]
}
```

After 0 seconds, i.e. right on start of the PET test, the string "D 1" will be sent the serial port.

After 1 second, "B -3600 400" will be sent and after 14 seconds, "D 0" will be sent.

The PetSerialCommands correspons to the PET test part of the exhibit and teh MRISerialCommands correspons to the MRI test part of the exhibit.

PETDoneSerialCommands is an array of commands to be sent whne PET test is done, which causes the device to get ready for a possible next PET test in the next exhibit run.

initSerialCommands is also an array of commands to be sent whne the exhibit loads, that are used to make sure all devices are initialized to their test start positions.

Finally, the PETRunTime nad MRIRunTime specifies the times in second for running the PET and MRI tests correspondintly. This is important as it allows the exhibit to continue, assuming the test was done, even if there was some physical issue with the device, thus still making the exhibit operational.

#### languages

This key provides an array of language objects defining all aspects related to all languages support by the exhibit (default is English, Arabic and Hebrew).

For each language object the prefix key sets its prefix used for other configuration parts (such as texts and defaultLanguage). This is he/ar/en by default.
Then, the rtl key specifies weather the language is right to left or left to right.
The buttonText specifies the text on the button to select that language.
Finally, the font object specifies different fonts for different types of texts and headers.
Each font key (such as headerFont or textFont) linkes to an object consisiting of a filename key, with the path to the file from root (i.e. assets/fonts/file.ttf) and the font size to be used (an integer).

To see all fonts keys and an example of a language object, observe this Hebrew language example:

```
{
    "prefix": "he",
    "rtl": true,
    "buttonText": "עברית",
    "fonts": 
    {
        "bigHeaderFont": {"filename": "assets/fonts/SimplerPro_V3-Black.ttf", "size": 144},
        "headerFont": {"filename": "assets/fonts/SimplerPro_V3-Black.ttf", "size": 72},
        "smallScreenHeaderFont": {"filename": "assets/fonts/SimplerPro_V3-Black.ttf", "size": 48},
        "subHeaderFont": {"filename": "assets/fonts/SimplerPro_V3-Bold.ttf", "size": 40},
        "subSubHeaderFont": {"filename": "assets/fonts/SimplerPro_V3-Bold.ttf", "size": 36},
        "smallScreenSubSubHeaderFont": {"filename": "assets/fonts/SimplerPro_V3-Bold.ttf", "size": 32},
        "textFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 40},
        "smallTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 30},
        "smallerTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 26},
        "smallButtonTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 24},
        "almostExtraSmallTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 22},
        "extraSmallTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 20},
        "smallScreenExtraSmallTextFont": {"filename": "assets/fonts/SimplerPro_V3-Regular.ttf", "size": 16}
    }
}
```

#### texts

This key contains all texts translations for each languages.
It is an object with key leading to an object.
Each key is the language prefix (as defined in the languages array) and leads to a key/value pair mapping.
Key is a set all capitals and underscore identifiers of various texts in the exhibits, and value is simply the translated text.
Note that some texts are multi-lines and so are separated by the '\n' special character.

See a partial example here:

```
"texts": {
    "en": {
        "RN_OPENING_SCREEN_HEADER": "Neuron Under Construction",
        "RN_OPENING_SCREEN_SUB_HEADER": "You are invited to reconstruct your own neuron",
        "RN_OPENING_SCREEN_BUTTON_TEXT": "Start",

        "DFAM_LEARN_MORE_BACK_BUTTON_TEXT": "Back",
        "DFAM_LEARN_MORE_HEALTHY_DESC_TEXT": "The tests do not seem to indicate the patient\nhas Alzheimer’s.\nThe MRI scan shows a normal brain. In Alzheimer’s,\ncells die throughout the brain so that the brain tissue\nbecomes thin, unlike the case of our patient.\n\nMany abilities related to drawing a clock, such as\nknowledge retrieval and management, are impaired in\nAlzheimer’s patients. However, our patient was able\nto draw a clock properly.\n\nThe PET scan indicating beta-amyloid plaques very\ncommon among Alzheimer’s patients (but not in healthy\nbrains) showed no red concentrations at all.\nMeaning, there are no beta-amyloid plaques in our\npatient’s brain, as opposed to what we would expect\nto find in an Alzheimer’s patient."
    },

    "ar": {
        "RN_OPENING_SCREEN_HEADER": "خلايا عصبية قيد الإنشاء",
        "RN_OPENING_SCREEN_SUB_HEADER": "أنتم مدعوون لبناء الخلية العصبية الخاصة بكم",
        "RN_OPENING_SCREEN_BUTTON_TEXT": "ابدأوا",

        "DFAM_LEARN_MORE_BACK_BUTTON_TEXT": "عودة",
        "DFAM_LEARN_MORE_HEALTHY_DESC_TEXT": "وفقًا للاختبارات، لا يبدو أن المريض مصاب بمرض الزهايمر.\n\nفي اختبار التصوير بالرنين المغناطيسي(MRI)، يبدو دماغه طبيعياً.\nفي الزهايمر خلايا في جميع أنحاء الدماغ تموت،\nوبالتالي فإن أنسجة الدماغ قليلة للغاية، على عكس المريض.\n\nهناك العديد من القدرات المرتبطة برسم الساعة،\nمثل استرجاع المعرفة والمهارات الإدارية ، تتضرر عند مرضى\nالزهايمر، لكن مع ذلك، نجح المريض في رسم الساعة بشكل جميل.\n\nلم يُظهر مسح PET الذي وضع علامة على مجموعات بيتا أميلويد \nالشائعة جدًا في أدمغة مرضى الزهايمر (ولكن ليس في أدمغة الأصحاء)\nأيّ مناطق حمراء على الإطلاق، مما يعني أن دماغ المريض لا يحتوي على\nتركيزات عالية من بيتا أميلويد، على عكس ما لوحظ في مرضى الزهايمر.",
    },

    "he": {
        "RN_OPENING_SCREEN_HEADER": "כאן בונים נוירון",
        "RN_OPENING_SCREEN_SUB_HEADER": "אתם מוזמנים לבנות נוירון משלכם",
        "RN_OPENING_SCREEN_BUTTON_TEXT": "התחילו",

        "DFAM_LEARN_MORE_BACK_BUTTON_TEXT": "אחורה",
        "DFAM_LEARN_MORE_HEALTHY_DESC_TEXT": "לפי הבדיקות לא נראה שלחולה יש אלצהיימר.\n\nבבדיקת ה-MRI המוח נראה תקין. באלצהיימר תאים בכל רחבי המוח מתים,\nולכן רקמת המוח מאוד דלילה, שלא כמו אצל החולה.\n\nיכולות רבות שקשורות בציור שעון, כמו שליפת ידע ויכולות ניהול,\nנפגעות אצל חולי אלצהיימר,\nאך עם זאת החולה הצליח לצייר שעון תקין.\n\nסריקת ה-PET שסימנה את צברי הבטא עמילואיד הנפוצים מאוד\nבמוחם של חולי אלצהיימר (אך לא במוחם של בריאים),\nלא הראתה אזורים אדומים כלל, כלומר במוחו של החולה אין\nריכוזים גבוהים של בטא עמילואיד, בניגוד למה שנצפה מחולה אלצהיימר."
    }
}
```

There are assisting text handling scripts that can convert from and to csv and auto-split long text, see designated section below for details.

#### openingVideos

This array describes all the buttons clickable in the opening exhibit, and what happens when you click them.
They contain info on all videos showing as well as the map and credits screen.

Each object has an **image** and **tappedImage** properties for specifying the images (under assets/images) used for the regular and tapped button graphics, as well as **x** and **y** specifying the top left corner of the button position.

In addition, the **textKey** properties states the text used to decide what will be written on the button as the description text.

Finally, the **type** key specifies weather the button shows a video, or is the credits or map screen.
This is done using the VIDOE, CREDITS or MAP values.

For the video type, a few other options are relevant:

The **file** key links to an ojbect showing the actual video filename path (i.e. assets/vidoes/file.mp4), keyed by the language prefix (as captions are included in the video file itself).

The **soundFile** specifies the same for the audio files, as the vidoe is played without sound, and needs a separate ogg file with the audio.

Finally, you can use a similar **fps** key (optional) to overwrite the default fps used for some videos. This is somtimes important for cases where the vidoes lack ftp info for some reason.

Here is a full example for a video button, with all options specified:

```
{
    "type": "VIDEO",
    "file": {
        "en": "assets/videos/opening/en-dancing-neuron.mp4",
        "he": "assets/videos/opening/he-dancing-neuron.mp4",
        "ar": "assets/videos/opening/ar-dancing-neuron.mp4"
    },
    "soundFile": {
        "en": "assets/videos/opening/en-dancing-neuron.ogg",
        "he": "assets/videos/opening/en-dancing-neuron.ogg",
        "ar": "assets/videos/opening/en-dancing-neuron.ogg"
    },
    "fps": {
        "en": 23,
        "he": 23,
        "ar": 23
    },
    "image": "dancing-neuron",
    "tappedImage": "dancing-neuron",
    "x": 960,
    "y": 500,
    "textKey": "OS_DANCING_NEURON_TEXT"
}
```

#### neuronPaths

This part of the configuration file saves all drawable paths in each neuron for the exhibit Neuron under Construction.
The object consist of a key for each neuron type, following an object containing an array of animationPaths and a select key.
The select key decides how many paths should be selected for drawing for the current neuron.
The animationPaths array is a full description of all neuron paths.
The paths are describe by a tree-like structure. Each path consists of a type (regular or dotted, if it should be dotted as an example), a path array with x and y objects sequentially creating a segmented line, and a nextPath array, consiting of more paths recursively.

Here is an example of a path defintiion:

```
"basket": {
    "animationPaths": [
        {
            "type": "regular",
            "path": [
                {"x": 306, "y": 258},
                {"x": 305, "y": 264},
                {"x": 306, "y": 267}
            ],
            "nextPaths": [
                {
                    "type": "regular",
                    "path": [
                        {"x": 306, "y": 267},
                        {"x": 308, "y": 271},
                        {"x": 309, "y": 276},
                        {"x": 312, "y": 280},
                        {"x": 313, "y": 285},
                        {"x": 314, "y": 290},
                        {"x": 314, "y": 296}
                    ]
                },
                {
                    "type": "dotted",
                    "path": [
                        {"x": 306, "y": 267},
                        {"x": 305, "y": 275},
                        {"x": 305, "y": 279},
                        {"x": 304, "y": 282},
                        {"x": 305, "y": 286},
                        {"x": 305, "y": 291},
                        {"x": 305, "y": 297},
                        {"x": 305, "y": 302},
                        {"x": 305, "y": 305}
                    ]
                }
            ]
        }
    ],
    "select": 2
}
```

#### mapCountries

Finally, the mapCountries key provides a country name to object mapping of all HBP dots for each country in the map screen, for the opening exhibit.
The mapped object provides the **nameKey** property specifying the country name key, and an **institutions** array.
The **institutions** array contains an object for each dot on the name, specifying the **mapX**, **mapY** coordinates, the **nameKey** for the key describing the institute,
a **cityKey** for the key describying the city, and a **cityY** and **descY** used to locate the y values of the city text and description text properly in the screen.

Here is an example key to object definition for Hungary:

```
"hungary": {
    "nameKey": "OS_MAP_COUNTRY_HUNGARY_NAME",
    "institutions": [
        {
            "mapX": 331,
            "mapY": 141,
            
            "nameKey": "OS_MAP_P30_NAME",
            "cityKey": "OS_MAP_P30_CITY",

            "cityY": 618,
            "descY": 675
        },
        {
            "mapX": 579,
            "mapY": 128,
            
            "nameKey": "OS_MAP_P15_NAME",
            "cityKey": "OS_MAP_P15_CITY"
        }
    ]
}
```

Note that the paths are generated out of the image using the create-paths.py script in root (see details in separate section below).

### Specific

Each exhibit can override some of the common configs.
This is mostly important to disable serial port on the opening screen and neuron under construction exhibits, which don't need it, and to set different touch parameters and screen sizes.

That is why the Doctor for a Moment config changes the screen size, enables touch and serialp port. This is called config-doctor.json.

The Neuron under Construction config just enables touch, in config-neuron.json.

And the Opening screen config enables touch and updates the touchMaxX and touchMaxY as the touch screen used is very big in this exhibit.

Finally, there is a special config-doctor-mouse.json that is used if you run the Doctor for a Moment exhibit with --mouse.
Then, it makes sure to disable touch, and give a slightly different screen size.

## Log

### Opening

The exhibit supports a rotating log named opening.log for the Opening exhibit. in the root directory, that logs the following events:
* START (the exhibit loads)
* INIT (exhibit initalization is done)
* PRELOAD_START (preloading videos start, so they are ready to play immediately)
* PRELOAD_DONE (preloading videos ends)
* PRELOADING_VIDEO_START,FILE (preloading of video filename FILE has started)
* PRELOADING_VIDEO_DONE,FILE (preloading of video filename FILE has ended)
* TRANSITION|CREDITS (credits was clicked)
* TRANSITION|COUNTRY|NAME (country named NAME was clicked)
* TRANSITION|MAP (map button was clicked)
* TRANSITION|START (moved back to start screen by video ending or home button)
* TRANSITION|VIDEO|{'file': 'FILENAME', 'soundFile': 'SOUND_FILENAME', 'hasBack': True/False, 'fps': FPS} (video with file FILENAME and sound file SOUND_FILENAME button was clicked on, hasBack states weather it has a back button and video will be palyed in the FPS specified)
* TRANSITION|INST_VIDEO|{'countryData': COUNTRY ,'file': FILENAME, 'soundFile': SOUND_FILENAME, 'fps': FPS} (institution video for in COUNTRY with file FILENAME and sound file SOUND_FILENAME button was clicked on, and will be palyed in the FPS specified)
* PLAY_START|FILENAME (vidoe named FILENAME started playing)
* PLAY_STOPPED (video play stopped by back button)
* PLAY_DONE (video ended playing completely)
* NEXT_INSTITUTION|COUNTRY|INST (next button was clicked to get to INST institution and COUNTRY country)
* PREV_INSTITUTION|COUNTRY|INST (prev button was clicked to get to INST institution and COUNTRY country)
* SELECT_INSTITUTION|COUNTRY|INST (institution INST in country COUNTRY was directly clicked)
* In case of an error, the message will consits the error message with its start trace

Each event will be prefixed by a timestamp (year-month-day hour:minute:seconds.mili with year as 4 digit, all rest as 2 digit and milliseconds as 3 digits), a | separator and then INFO or ERROR, another | separator, OPENING, another | separator, then the memory size the exhibit takes in MB (i.e. 100MB), and finally another | separator, then the actual message specified above.

So a sample line will look like this (note the timestamp format, that includes milliseconds):
```
2023-03-15 14:45:30.123|INFO|OPENING|10MB|START|en
```

### Neuron under Construction

The exhibit supports a rotating log named neuron.log for the Neuron under Construction exhibit. in the root directory, that logs the following events:
* START (the exhibit loads)
* INIT (exhibit initalization is done)
* PRELOAD_START (preloading videos start, so they are ready to play immediately)
* PRELOAD_DONE (preloading videos ends)
* PRELOADING_VIDEO_START,FILE (preloading of video filename FILE has started)
* PRELOADING_VIDEO_DONE,FILE (preloading of video filename FILE has ended)
* TRANSITION|START (start screen was shown)
* TRANSITION|CHOOSE (choose nueron screen was moved to)
* TRANSITION|DRAW|NEURON (neuron NEURON was chosen to draw)
* TRANSITION|SUMMARY|NEURON (neuron NEURON summary was presented)
* PLAY_START|FILENAME (vidoe named FILENAME started playing)
* PLAY_DONE (video ended playing completely)
* DRAW_ANIMATION_START (drawing animation help started)
* DRAW_ANIMATION_END (drawing animation help ended)
* DRAW_START (mouse drawing started)
* DRAW_WRONG|DIST (mouse drawing ended wrongly, because distance was too far)
* DRAW_WRONG|NO_DRAW (mouse drawing ended wrongly, because no drawing was actually done)
* DRAW_CORRECT|N (draw was correct for path number N, 1-based)
* MODEL (neuron model was shown)
* LIGHTNING (neuron lighting was clicked on)
* In case of an error, the message will consits the error message with its start trace

Each event will be prefixed by a timestamp (year-month-day hour:minute:seconds.mili with year as 4 digit, all rest as 2 digit and milliseconds as 3 digits), a | separator and then INFO or ERROR, another | separator, NEURON, another | separator, then the memory size the exhibit takes in MB (i.e. 100MB), and finally another | separator, then the actual message specified above.

So a sample line will look like this (note the timestamp format, that includes milliseconds):
```
2023-03-15 14:45:30.123|INFO|NEURON|10MB|START|en
```

### Doctor for a Moment

The exhibit supports a rotating log named neuron.log for the Neuron under Construction exhibit. in the root directory, that logs the following events:
* INIT (exhibit initalization is done)
* PRELOAD_START (preloading videos start, so they are ready to play immediately)
* PRELOAD_DONE (preloading videos ends)
* PRELOADING_VIDEO_START,FILE (preloading of video filename FILE has started)
* PRELOADING_VIDEO_DONE,FILE (preloading of video filename FILE has ended)
* TRANSITION|OPENING_VIDEO (opening video started)
* TRANSITION|EXPLANATION (explanation screen is shown after opening video)
* TRANSITION|CHOOSE (choose test screen was moved to)
* TRANSITION|CHOOSE (choose test screen was moved to)
* TRANSITION|DIAGNOSE (diagnose button was clicked)
* TRANSITION|RUN_TEST|{'test': 'TEST', 'isHealthy': True/Flase} (test TEST was run, isHealthy specifies if patient is healthy or not)
* TRANSITION|TEST_RESULTS|{'test': 'TEST', 'isHealthy': True/False} (test results for TEST was shown, isHealthy specifies if patient is healthy or not)
* TRANSITION|EVALUATE|{'condition': True/False, 'diagnosys': True/False} (evaluation was done, with specified condition and diagnosys)
* TRANSITION|RESET (start again with another patient)
* TRANSITION|LEARN_MORE|{'condition': True/False, 'diagnosys': True/False} (learn more was click with the specified condition and diagonsys)
* PLAY_START|FILENAME (vidoe named FILENAME started playing)
* PLAY_DONE (video ended playing completely)
* In case of an error, the message will consits the error message with its start trace

Each event will be prefixed by a timestamp (year-month-day hour:minute:seconds.mili with year as 4 digit, all rest as 2 digit and milliseconds as 3 digits), a | separator and then INFO or ERROR, another | separator, DOCTOR, another | separator, then the memory size the exhibit takes in MB (i.e. 100MB), and finally another | separator, then the actual message specified above.

So a sample line will look like this (note the timestamp format, that includes milliseconds):
```
2023-03-15 14:45:30.123|INFO|DOCTOR|10MB|START|en
```

## Serial Port Interface
The Neuron under Construction exhibit requires a serial port connection to a phsyical simuation of both the PET and MRI tests.

Details on the interpertation of the commands are not part of this software implementation.
However, it is important to know that there are initialization comamnds sent when the exhibit loads, and that throughout the test, at specific seconds from the test start, several commands are sent.

Finally, there are some finalization commands needed to be sent when the PET test is done.
Also, the times of the tests are defined by seconds, so the exhibit won't be stuck if the physical device is stuck.

For detailed information on where each command is defined, see the Config section above.

## Text Handling Scripts

As described in the config section above, all the text keys and translations are defined in the configuration file.
Hwoever, it is quite hard to edit it directly by translators.

To make the translation easier, two scripts are used in the assets/config directory: extract-translation-csv.py and update-config-translations.py.

The first script is used to extract a csv from the current config.
Run it with:

```
python3 extract-translation-csv.py
```

Then, the translate.csv file will be created.
Now you can edit the csv for changes, and when done, update the config by running the update-config-translations.py script, like this:

```
python3 update-config-translations.py
```

When running both scripts make sure to do that from the assets/config directory as they search for all file names locally.

Finally, another useful text scripts is the auto-break-lines.py script.

This script effectively opens up all texts, and separates them to up to 70 characters per line.
As of now, the lines are splitted correctly, and that shows in the csv as well, so there is no need to run this script, unless massive texts are changed.
This script was run at the beginning, while developing, to get an initial linse partition easily.

## Creating Neuron Paths

As described under the config section, the Neuron under Construction uses a full description of all parts, per neuron type.
These paths are hard to define manually, therefore, there is a script called create-paths.py in the root of the Exhibits dir, used to create them from images.

To use the script, first, choose a neuron image that has colored dots already marked of paths (such as martinotti-color.png under assets/images/neuron).
Then run the script with the image name only, without extension or path, like this:

```
python3 create-paths.py martinotti-color
```

Now you can click on dots one after the other, and click the **'s'** key when a path is done. Then, it will be saved to a path-1.txt file (or path-2.txt if it's the second, etc...).
This way, you can trace many paths, then construct them manually to the config file format.

Note that this hard work has already been done for this exhibit, and no configurations should change, unless new neurons are introduced etc.

## Video Generation

Besides the code directory in the repository, there is a video-generation folder.
This contains some blender neuron models used to export the 3D spinning neuron sequence.
Please take a look at the **generate-blender.txt** file on how they were rendered, if this is ever needed again.
The already generated frames exists under assets/videos/neuron/animations and then in a dir for each big and small neuron, and electric or not.

## Brain Atlas Translations

The Brain Atlas is an exhibit received with no code, already written and ready to run.
However, it needed translations.

To translate, we received a .json file for each language, that needs to be exported and embedded in the atlas by the developers.
To do so, we created a few scripts for the task, all under the code/BrainAtlasJsonFiles directory.

First, use extract-translation-csv.py following by all json files for each language, to get a csv, like this:

```
python3 extract-translation-csv.py AtastText_arabic.json AtlasText_english.json AtlasText_hebrew.json
```

Then, a translate.csv file is created which you can edit.

Finally, to get the json files back, use create-translation-json.py scripts like this:

```
python3 create-translation-json.py translate.csv
```

And the json files will be created accordingly, with the .new prefix added to them (to not overwrite old ones).
Then they can be tested and finally manually overridden.