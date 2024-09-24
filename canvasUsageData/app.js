let start = Date.now(); // Set a start time - used to determine timeframe of generating usage data for a single user
let domain = 'https://<INSTITUTION-NAME>.instructure.com'; // Domain name of Canvas instance where you are generating usage data
let user = '<USERNAME>'; // Test user username
let password = '<PASSWORD>'; // Test user password
let courses = ["<COURSE-IDs"]; // Array of course Canvas IDs
let refreshMax = 10; // Set boundaries on random refresh occurences
let refreshMin = 3;

const puppeteer = require('puppeteer');
console.log("Launch puppeteer");

// Function used to generate a random integer between provided max and min values. Generates more realistic usage data.
function randomIntFromInterval(min, max) {
  return Math.floor(Math.random() * (max - min + 1) + min)
}

(async () => {
    const browser = await puppeteer.launch({executablePath: '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome', headless: "new"});
    console.log("Launched Chrome");

    const page = await browser.newPage(); 
    await page.goto(domain +"/login/canvas"); // Open a new window in Chrome and navigate to the relevant Canvas login

    await page.type('#pseudonym_session_unique_id', user);
    await page.type('#pseudonym_session_password', password);

    await Promise.all([
        await page.click('input.Button.Button--login'),
        page.waitForNavigation({waitUntil: 'networkidle0'})
    ]);    

    // Loop through full Courses array
    for (let x = 0; x < courses.length; x++){
        
        await page.goto(domain+"/courses/" + courses[x]); // Navigate to course landing page
        
        // Course homepage reload random number of times 
        for (let i = 0; i < randomIntFromInterval(refreshMin, refreshMax); i++){
            await page.reload({waitUntil: 'load'})
        };

        // Navigate to Modules
        await page.waitForSelector('a.modules');
        await page.evaluate(()=>document.querySelector('a.modules').click());

        // Re-use lines 43-44 with relevant JS selectors to click on specific module items. This will generate the desired page view data and/or engagement data.

        console.log("Course " + courses[x] +" complete!");
    };

    console.log("Testing completed successfully");
    let timeTaken = Date.now() - start;
    console.log("Total time taken: " + timeTaken + " milliseconds");
    await browser.close();

})();
