exports.handler = async (event, context) => {
    const { exec } = require("child_process");
    exec("python website_change_detector.py", (error, stdout, stderr) => {
        if (error) {
            console.error(`Error: ${error.message}`);
            return;
        }
        if (stderr) {
            console.error(`Stderr: ${stderr}`);
            return;
        }
        console.log(`Stdout: ${stdout}`);
    });
    return {
        statusCode: 200,
        body: "Change detection triggered!",
    };
};
