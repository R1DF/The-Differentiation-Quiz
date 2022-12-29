# Languages
_The Differentiation Quiz_ comes with 2 preinstalled languages: English and Russian.<br>
However, it is also possible to create your own.

## Making your own language
Making your language is easy - Simply copy any `.toml` language file (preinstalled ones are the best option) to use as a template and
translate all text in speech quotes to your own language. Be mindful of possible differences in grammar and context.<br><br>
You **must** also update its metadata at the top, as if it lacks a specific keyword then it will not be detected by the game.<br>
Any mistake in the language file's structure could read to an error.

### Testing and sharing
You can test out your language by simply setting it inside your game and checking how it works.<br>
You can share your language with anyone by simply sending the `.toml` file to them.<br>
**NOTE: ONLY A SMALL TOML FILE IS REQUIRED FOR THE LANGUAGE TO BE INSTALLED. If the author demands more, then they are lying to you.**

### Detecting
To make the game detect the language, simply move its file inside the `lang` folder where the game is installed.<br>
It will be detected, **but** it lacks the mandatory metadata then it will not be read.

## Preinstalled languages list
| Language | File | Link (for download) |
| -------- | ---- | ------------------- |
| English | `en.toml` | [link](https://raw.githubusercontent.com/R1DF/The-Differentiation-Quiz/master/src/lang/en.toml) |
| Russian | `ru.toml` | [link](https://raw.githubusercontent.com/R1DF/The-Differentiation-Quiz/master/src/lang/ru.toml) |
