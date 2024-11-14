import aboutstyle from "/src/styles/AboutUs.module.css"
import { useNavigate } from "react-router-dom";

function AboutUs() {

  const navigate = useNavigate();

  const trades = () => {
    navigate("/transactions");
  }

  return (
    <div className={aboutstyle.container}>
      {/* About Section */}
      <section className={aboutstyle.about}>
        <h1>About Capitol Gains</h1>
        <div className={aboutstyle.cardContainer}>
          {/* Mission Card */}
          <div className={aboutstyle.card}>
            <h2>Our Mission</h2>
            <p>
              Capitol Gains is on a mission to bring transparency to the world of political stock trading. 
              We're not just another finance app - we're the watchdogs of Wall Street and Washington, all rolled into one sleek platform.
            </p>
            <p>
              Our goal? To help you track politicians' trades faster than they can say "insider trading."
              (Just kidding, we're sure it's all above board... right?)
            </p>
            <p>🚀 Because knowledge is power, and power is... well, you know the rest.</p>
          </div>

          {/* Team Card */}
          <div className={aboutstyle.card}>
            <h2>The Team Behind the Trades</h2>
            <p>
              We’re Team 11, the cursed team who has come back with a vengeance to avenge all Team 11s that came before us.
              Some say we’re unlucky, but we prefer to think of ourselves as the "Spinal Tap" of coding teams - we go to 11!
            </p>
            <p>Our team motto: "May our code be as clean as our politicians' trading records." (We're still working on both.)</p>
            <p className={aboutstyle.highlight}>🏆 Proudly procrastinating on our CS506 project at UW-Madison</p>
          </div>
        </div>
      </section>

      {/* What We Do Section */}
      <section className={aboutstyle.whoWe}>
        <h2>What We Do</h2>
        <p>
          Capitol Gains is a platform that tracks American politicians' stock trades, ensuring transparency and enabling 
          the public to make informed decisions. We scrape data daily from websites tracking congressional stock trades, 
          parse it into a structured format, and store it in our database.
        </p>
        <p>
          Using Python (Django) for the backend and React for the frontend, we allow users to view, filter, and analyze 
          trading activities of different groups of politicians. Want to know if your local representative is bullish on tech stocks? 
          We've got you covered!
        </p>

        {/* Key Features */}
        <div className={aboutstyle.features}>
          <h3>Key Features</h3>
          <ul>
            <li>Daily updates of politician trading activities</li>
            <li>Filter trades by political party, chamber, or individual politicians</li>
            <li>Analyze trading patterns and performance</li>
            <li>Track your favorite politicians (or least favorite, we don't judge)</li>
            <li>Compliance with the 2012 STOCK Act</li>
          </ul>
        </div>
      </section>

      {/* Our Customers Section */}
      <section className={aboutstyle.customers}>
        <h2>Our Customers</h2>
        <p>
          While we’re primarily developing this application for our professor and TAs (hello, easy A!), we have bigger dreams. 
          We’re designing Capitol Gains for the public - for anyone who wants to keep tabs on the stock market savvy (or lack thereof) 
          of their elected officials.
        </p>
        <p>
          Our platform aims to provide transparency, enabling users to rank politicians by their stock market earnings 
          and gain insights from congressional trading patterns. Because let’s face it, who doesn’t want to know if their 
          senator is better at picking stocks than they are?
        </p>
        <div className={aboutstyle.buttonGroup}>
          <button onClick={trades}>Explore Trades</button>
        </div>
      </section>

      
      <footer className={aboutstyle.footer}>
        <p>© 2024 Capitol Gains. All rights reserved. No politicians were harmed in the making of this website.</p>
        <p>Disclaimer: This is a school project. Please don’t sue us, we’re just poor students.</p>
      </footer>
    </div>
  );
}

export default AboutUs;

