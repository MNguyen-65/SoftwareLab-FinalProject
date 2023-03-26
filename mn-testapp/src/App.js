import React, { useState } from 'react';
import axios from 'axios';

function App() {
  const [loggedIn, setLoggedIn] = useState(false);
  const [username, setUsername] = useState('');
  const [userid, setUserid] = useState('');
  const [password, setPassword] = useState('');
  const [firstName, setFirstName] = useState('');   // TODO: unnecessary
  const [lastName, setLastName] = useState('');     // TODO: unnecessary
  const [email, setEmail] = useState('');           // TODO: unnecessary
  const [inventory, setInventory] = useState([]);   // TODO: implement later on
  const [itemToAdd, setItemToAdd] = useState('');
  const [itemQuantity, setItemQuantity] = useState(0);
  const [userItems, setUserItems] = useState({});
  const [success, setSuccess] = useState(false);


  const handleLogin = () => {
    axios.post('/login', {username: username, userid: userid, password: password})
      .then(res => {
        if (res.data.success) {
          setSuccess(true);
        } else {
          alert(res.data.message); // Might want to return error message
        }
      })
      .catch(err => {
        console.log(err);
      });
  };


  const handleAddUser = () => {
    axios.post('/add_user', {username: username, userid: userid, password: password})
      .then(res => {
        if (res.data.success) {
          setSuccess(true);
        } else {
          alert(res.data.message);
        }
      })
      .catch(err => {
        console.log(err);
      });
  };

  const handleRefreshProjects = () => {
    axios.get('/get_projects')
      .then(response => {
        setUserItems(response.data);
      })
      .catch(error => {
        console.log(error);
      });
  };

  const handleCheckIn = () => {
    axios.post('/check_in', {username: username, item_name: itemToAdd, quantity: itemQuantity})
      .then(response => {
        if (response.data.success) {
          alert(response.data.message);
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
  };

  const handleCheckOut = () => {
    axios.post('/check_out', {username: username, item_name: itemToAdd, quantity: itemQuantity})
      .then(response => {
        if (response.data.success) {
          alert(response.data.message);
        } else {
          alert(response.data.message);
        }
      })
      .catch(error => {
        console.log(error);
      });
  };

  
  return (
    <div>
      {!success && (
        <div>
          <h2>Login</h2>
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
          <br />
          <input type="text" placeholder="UserID" value={userid} onChange={e => setUserid(e.target.value)} />
          <br />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
          <br />
          <button onClick={handleLogin}>Login</button>
          <br />
          <h2>Add User</h2>
          <input type="text" placeholder="Username" value={username} onChange={e => setUsername(e.target.value)} />
          <br />
          <input type="text" placeholder="UserID" value={userid} onChange={e => setUserid(e.target.value)} />
          <br />
          <input type="password" placeholder="Password" value={password} onChange={e => setPassword(e.target.value)} />
          
          {/* TODO: remove unnecessary fields */}
          <br />
          <input type="text" placeholder="First Name" value={firstName} onChange={e => setFirstName(e.target.value)} />
          <br />
          <input type="text" placeholder="Last Name" value={lastName} onChange={e => setLastName(e.target.value)} />
          <br />
          <input type="text" placeholder="Email" value={email} onChange={e => setEmail(e.target.value)} />
          <br />
          <button onClick={handleAddUser}>Add User</button>
        </div>
  )}
  {success && (
    <div>
      <h2>Inventory</h2>
      {/* <button onClick={handleRefreshProjects}>Refresh Projects</button>
      <ul>
        {inventory.map(item => (
          <li key={item.name}>
            {item.name}: {item.quantity}
          </li>
        ))}
      </ul> */}
      <h2>Check In</h2>
      <input type="text" placeholder="Item Name" value={itemToAdd} onChange={e => setItemToAdd(e.target.value)} />
      <br />
      <input type="number" placeholder="Quantity" value={itemQuantity} onChange={e => setItemQuantity(parseInt(e.target.value))} />
      <br />
      <button onClick={handleCheckIn}>Check In</button>
      <h2>Check Out</h2>
      <input type="text" placeholder="Item Name" value={itemToAdd} onChange={e => setItemToAdd(e.target.value)} />
      <br />
      <input type="number" placeholder="Quantity" value={itemQuantity} onChange={e => setItemQuantity(parseInt(e.target.value))} />
      <br />
      <button onClick={handleCheckOut}>Check Out</button>
      <h2>My Projects</h2>
      <button onClick={handleRefreshProjects}>Refresh Projects</button>
      {/* <ul>
        {userItems.map(project => (
          <li key={item}>
            {item}
          </li>
        ))}
      </ul> */}

      {/* <ul>
        {console.log("137 debug react")}
        {console.log(userItems)}
        {userItems.map(([name, description, projectid]) => (
          <li key={name}>
            {name}: {description}
          </li>
        ))}
      </ul> */}
    </div>
  )}
</div>
);
}

export default App;
