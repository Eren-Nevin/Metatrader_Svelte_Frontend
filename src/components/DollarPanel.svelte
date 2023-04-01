<script>
  import { DollarStore, sendStateToServer } from "../stores.js";
  import { DollarPrice } from "../models.js";
  import Button from "./Button.svelte";
  import Card from "./Card.svelte";

  let manual_rate = "";

  let user_selected_timedate;

  const handleSubmitNewDollarPrice = async (new_price) => {
    console.log(new_price);

    DollarStore.update((currentState) => {
      let new_historic_price = new DollarPrice(
        +currentState.current_price.price,
        currentState.current_price.timestamp
      );
      let new_historic_prices = [
        new_historic_price,
        ...currentState.historic_prices,
      ];

      console.log(user_selected_timedate);

      let new_dollar_price = new DollarPrice(
        new_price,
        user_selected_timedate instanceof String
          ? Math.floor(Date.parse(user_selected_timedate) / 1000)
          : Math.floor(new Date() / 1000)
      );

      let new_state = {
        current_price: new_dollar_price,
        historic_prices: new_historic_prices,
      };

      return new_state;
    });

      await sendStateToServer()
  };

  const convertTimestampToDate = (timestamp) => {
    let pointInTime = new Date(timestamp * 1000);
    return pointInTime.toLocaleDateString();
  };

  const convertTimestampToTime = (timestamp) => {
    let pointInTime = new Date(timestamp * 1000).toLocaleTimeString();

    return pointInTime;
  };
</script>

<Card>
  <form on:submit|preventDefault={handleSubmitNewDollarPrice(manual_rate)}>
    <div style="display: flex;">
      <p>Enter</p>
      <input type="number" min="0" bind:value={manual_rate} />
      <p>$</p>
      <input type="datetime-local" bind:value={user_selected_timedate} />
      <Button type="submit">Add</Button>
    </div>
  </form>

  <hr class="solid" />

  <div style="display: flex; justify-content: space-between;">
    <p>
      Current Price:
      {$DollarStore.current_price.price}
    </p>
    <p>
      {convertTimestampToDate($DollarStore.current_price.timestamp)} -
      {convertTimestampToTime($DollarStore.current_price.timestamp)}
    </p>
  </div>

  <hr class="solid" />

  <p>Logs:</p>
  {#each $DollarStore.historic_prices as dollar (dollar.uid)}
    <div style="display: flex; justify-content: space-between; ">
      <p>{dollar.price}</p>
      <p>
        {convertTimestampToDate(dollar.timestamp)} -
        {convertTimestampToTime(dollar.timestamp)}
      </p>
    </div>
  {/each}
</Card>

<style>
  * {
    font-size: 16px;
    margin-right: 8px;
    margin-top: 4px;
    margin-bottom: 4px;
  }

  input[type="number"] {
    width: 120px;
    border-width: 1px;
    border-radius: 4px;
    text-align: center;
    padding: 2px 4px;
    /* flex-grow: 2; */
    /* border: none; */
    font-size: 16px;
    text-align: start;
  }

  input:focus {
    outline: none;
  }

  hr.solid {
    border-top: 1px solid #bbb;
    margin: 8px 0px;
  }
</style>
