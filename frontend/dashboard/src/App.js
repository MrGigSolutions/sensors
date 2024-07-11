import logo from './logo.svg';
import './App.css';

import React from "react";
import { useState,} from 'react'

import ReactApexChart from "react-apexcharts";
import { RouterProvider, createBrowserRouter } from 'react-router-dom'
import useSWR from 'swr';


const Dashboard = ({user, parentHandleLogout}) => {
  return (
    <>
      <h3>Dashboard</h3>
      <button className="btn" onClick={parentHandleLogout}>
        Logout
      </button>
      <h4>{user?.name}</h4>
      <br />
      <p>{user?.email}</p>
      <br />
      <div>
        <Graph/>
      </div>
    </>
  )
}

const Login = ({parentHandleLogin}) => {
  const handleLogin = async () => {
    try {
      const login_details = fetch(
      "http://localhost:8080/auth/token",
        {
           method: "POST",
           headers: {
             "Content-Type": "application/x-www-form-urlencoded"
           },
           body: "grant_type=password&username=johndoe&password=secret"
        }
      ).then((res) => res.json())
      parentHandleLogin(login_details.username)
    } catch (err) {
      console.error(err)
    }
  }
  return (
    <>
      <h3>Login to Dashboard</h3>
      <button className="btn" onClick={handleLogin}>
        Login
      </button>
    </>
  )
}

const Home = () => {
  const [ loggedIn, setLoggedIn] = useState(false);
  const [ user, setUser ] = useState(null);
  const handleLogout = () => {
    setLoggedIn(false);
    setUser(null);
  }

  const handleLogin = (user) => {
    setUser(user);
    setLoggedIn(true);
  }

  if (loggedIn === true) return <Dashboard user={user} parentHandleLogout={handleLogout} />
  if (loggedIn === false) return <Login parentHandleLogin={handleLogin}/>
  return <></>
}

const router = createBrowserRouter([
  {
    path: '/',
    element: <Home />,
  },
])

// created function to handle API request
const fetchWithSeconds = (url, seconds) => fetch(
    url + "?" + new URLSearchParams({seconds: seconds}).toString()
).then((res) => res.json());

function App() {
  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <RouterProvider router={router} />
      </header>
    </div>
  )
}

function Graph() {
  // TODO: Change this to be determined by the chart scale
  const seconds = 600;
  const transform = (json_data) => {

    const machine_names = json_data.map((machine_reading) => {
      return machine_reading["machine"]
    })
    const machine_series = machine_names.filter((machine, index) => machine_names.indexOf(machine) === index)

    return {
      type: 'line',
      options: {
        chart: {
            animations: {
                enabled: false,
                easing: 'easeinout',
                speed: 800,
                animateGradually: {
                    enabled: true,
                    delay: 150
                },
                dynamicAnimation: {
                    enabled: false,
                    speed: 350
                }
            }
        },
        dropShadow: {
          enabled: true,
          color: '#000',
          top: 18,
          left: 7,
          blur: 10,
          opacity: 0.2
        },
        xaxis: {
          type: 'datetime',
        }
      },
      series: machine_series.map((machine)=> {
        return {
          name: machine,
          data: json_data.filter((reading)=> reading.machine === machine).map(
              (reading) => {
            return {
              x: reading["timestamp"],
              y: reading["vibration_speed"]
            };
          })
        };
      })
    }
  };
  const {
    data,
    error,
    isValidating,
  } = useSWR(
      ['http://localhost:8080/sensor/data', seconds],
      ([url, seconds]) => fetchWithSeconds(url, seconds),
      { refreshInterval: 60000 }
  );


  // Handles error and loading state
  if (error) return <div className='failed'>failed to load</div>;
  if (isValidating) return <div className="Loading">Loading...</div>;

  const transformed_data = transform(data);

  return (
    <div className="app">
      <div className="row">
        <div className="mixed-chart">
          <ReactApexChart
            options={transformed_data.options}
            series={transformed_data.series}
            type={transformed_data.type}
            width="500"
          />
        </div>
      </div>
    </div>
  );
}

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }
//
export default App;
