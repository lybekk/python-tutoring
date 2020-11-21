async function createTables() {
    const data = {
        action: "make a table for our students",
    }
    await createStuff(data)
    location.reload()
}

async function deleteStudent(studentId) {
    const data = {
        action: "delete student",
        student_id: studentId
    }
    await createStuff(data)
    location.reload()
}

async function insertSampleData() {
    const response = await fetch('/insert/sample-data', {
        method: "POST"
    })
    const result = await response.text();
    if (response.ok) {
        location.reload()
    } else {
        console.log(result)
        printToInfoBox(result)
    }
}

async function dropDatabase() {
    const data = {
        action: "delete everything"
    }
    await createStuff(data)
    location.reload()
}

async function createStuff(data) {
    console.log("Sending POST request to server")
    try {
        const url = "/create/stuff"
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(data) // body data type must match "Content-Type" header
        });
        const result = await response.json(); // parses JSON response into native JavaScript objects
        if (result.ok) {
            console.log("Success", result)
            printToInfoBox("Success" + JSON.stringify(result))
        } else {
            const txt = "That didn't work" + JSON.stringify(result);
            console.log(txt)
            printToInfoBox(txt)
        }
    } catch (error) {
        const txt = "Something went wrong" + error;
        console.log(txt)
        printToInfoBox(txt)
    }
}

function printToInfoBox(text) {
    const container = document.getElementById("infoBox");
    container.innerText = text;
}

function showReloadButton() {
    const btn = document.getElementById("reloadBtn");
    btn.classList.remove("hidden")
}