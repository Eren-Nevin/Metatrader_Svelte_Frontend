<script>
  import Card from "./Card.svelte";
  import { BotStore, sendStateToServer } from "../stores";
  import {onMount} from "svelte";

  const onTriggerChange = async (e) => {
    let selected = +e.currentTarget.value;
    BotStore.update((currentState) => {
      let new_state = JSON.parse(JSON.stringify(currentState));

      if (selected === 1) {
        new_state.onTime = true;
        new_state.onChange = false;
      } else {
        new_state.onTime = false;
        new_state.onChange = true;
      }

      return new_state;
    });
    await sendStateToServer();
  };

    const onIntervalChangeHandler = async () => {
        await sendStateToServer();
    }

  const onBotDisableButtonClicked = async () => {
    $BotStore.disabled = !$BotStore.disabled;
      await sendStateToServer();
  };

    onMount(async () => {
        console.log("MOUNTED BOT PANEL")
        console.log($BotStore.onTime)
        console.log($BotStore.onChange)
    })

</script>

<Card>
  <div style="display: flex;">
    <p>Status:</p>
    <p>{$BotStore.disabled ? "Disabled" : "Running"}</p>
  </div>
  {#if !$BotStore.disabled}
    <ul class="rating">
      <li>
        <input
          type="radio"
          id="by-time"
          name="by-time"
          value="1"
          on:change={onTriggerChange}
          checked={$BotStore.onTime}
        />
        <label for="num1">Send On Time</label>
      </li>
      <li>
        <input
          type="radio"
          id="by-change"
          name="by-change"
          value="2"
          on:change={onTriggerChange}
          checked={$BotStore.onChange}
        />
        <label for="num2">Send On Change</label>
      </li>
    </ul>
    {#if $BotStore.onTime}
      <div style="display: flex;">
        <p>Every</p>
        <input
          type="number"
          min="0"
          step="1"
          on:change={onIntervalChangeHandler}
          bind:value={$BotStore.interval.value}
        />
        <select
          bind:value={$BotStore.interval.unit}
          on:change={onIntervalChangeHandler}
          name="interval-unit"
          id="interval-unit"
        >
          <option value="Min">Minutes</option>
          <option value="Hour">Hours</option>
          <option value="Day">Days</option>
        </select>
      </div>
    {/if}
  {/if}
  <div style="display: flex">
    <button on:click={onBotDisableButtonClicked}>
      {$BotStore.disabled ? "Enable" : "Disable"}
    </button>
  </div>
</Card>

<style>
  * {
    font-size: 16px;
    margin-right: 8px;
    margin-top: 4px;
    margin-bottom: 4px;
  }
  .rating {
    display: flex;
    align-items: center;
    justify-content: left;
  }

  button {
    color: #fff;
    border: 0;
    border-radius: 8px;
    color: #fff;
    height: 32px;
    width: 120px;
    cursor: pointer;
    background-color: #202142;
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
