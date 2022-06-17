var say = require("say");
var voiceName = "voice_nick1"

say.speak("Luke, I am your father", voiceName, 0.75 , (err) => {
    if (err) {
        return console.error(err);
    }

    console.log(`Text with the voice ${voice}`);
});