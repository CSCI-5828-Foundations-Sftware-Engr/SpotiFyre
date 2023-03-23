import './App.css';

function App() {

  const handleSubmit = (event) => {
    event.preventDefault();
    // try {
    //   fetch("http://zelda.local:8080/?hello="+event.target.name.value, {
    //   headers: { 'Content-Type': 'application/json' },
    //   mode: "no-cors"
    // });

      
    // } catch (err) {
    //   console.log(err);
    // }
    console.log(event.target.name.value)
    alert('Hi '+ event.target.name.value)

    
  };

  return (
    <div className="wrapper">
      <form onSubmit={handleSubmit}>
        <fieldset>
          <label>
            <p>Name</p>
            <input name="name" />
          </label>
        </fieldset>
        <button type="submit">Submit</button>
      </form>
    </div>
  );
}

export default App;
