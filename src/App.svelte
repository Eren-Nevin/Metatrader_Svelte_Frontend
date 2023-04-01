<script>
  import { getAppStateFromServer } from "./stores";
  import { onMount } from "svelte";
  import Panel from "./components/Panel.svelte";

  let update_interval_ms = 30000;

  onMount(async () => {
    console.log("Loaded!");
    let appState = await getAppStateFromServer(23231);
    console.log(appState);

    /* const interval = setInterval(reloadRatesFromServer, update_interval_ms); */
    /* await reloadStateFromServer(); */
    /* return () => { */
    /*   clearInterval(interval); */
    /* }; */
  });
</script>

<main class="container">
    <div class="text-grey">Goals Overview</div>

  <div style="display: grid; grid-template-areas: 'a b' 'c d';">
    <Panel />
    <Panel />
    <Panel />
    <Panel />
  </div>
</main>

<style>
  * {
    font-size: 17px;
    font-family: Encode Sans,sans-serif;
  }

  .container {
    background-color: #242426;
  }

  .text-grey {
      color: rgb(156 163 175);
  }

  button {
    /* color: #fff; */
    margin: 0px 8px;
    border: 0;
    border-radius: 8px;
    /* color: #fff; */
    height: 48px;
    width: 120px;
    cursor: pointer;
    background-color: #69f0ae;
  }

  button:hover {
    transform: scale(0.98);
    opacity: 0.9;
  }

  button:disabled {
    background-color: #cccccc;
    color: #333;
    cursor: auto;
  }

  button:disabled:hover {
    transform: scale(1);
    opacity: 1;
  }
</style>
