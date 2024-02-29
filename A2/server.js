let express = require('express');
let fs = require('fs');

app = express();

function copyFile(copy) {
    fs.readFile("original.txt", "utf8", function(err,data) {
        
        for (let i = 0; i < copy; i++) {
            fs.writeFileSync("copy_" + (i+1) + ".txt", data);
            console.log(i);
        }
        
        console.log("Done copying " + copy + " files!");
    })
}

//copyFile(6);

app.get('/:number', function(req, resp){
    let copy = parseInt(req.params.number);
    copyFile(copy);
    resp.send("Done copying " + copy + " files!");
});


app.listen(3000);