<script>
  import { CurrencyStore, sendStateToServer } from "../stores";
  import { CurrencyRate } from "../models";
  import Card from "./Card.svelte";
  import { onMount } from "svelte";
  $: selectedCurrency = "";

  let updated_current_currencies;

  $: addingNewCurrency = true;

  $: newOrEditCurrency = {
    currencyCode: "",
    alias_name: "",
    rate: 1,
    has_manual_rate: true,
    manual_rate: 1,
    adjustment: 0,
  };

  const updateAddingNewCurrency = (currencyCode) => {
    let current_currencies_codes = updated_current_currencies.map(
      (v) => v.currencyCode
    );
    if (current_currencies_codes.includes(currencyCode)) {
      addingNewCurrency = false;
    } else {
      addingNewCurrency = true;
    }
  };

  const onNewFieldChangeHandler = (event) => {
    updateAddingNewCurrency(newOrEditCurrency.currencyCode);
  };

  const handleDeleteCurrency = async () => {
    console.log(`Deleting ${newOrEditCurrency}`);
    CurrencyStore.update((currentState) => {
      let newState = currentState;

      let newCurrencyRates = newState.currency_rates.filter(
        (currency_rate) =>
          currency_rate.currencyCode != newOrEditCurrency.currencyCode
      );

      newCurrencyRates = newCurrencyRates.filter((item) => item);

      newState.currency_rates = [...newCurrencyRates];

      resetNewOrEditCurrency();
      return newState;
    });
    await sendStateToServer();
  };

  const handleAddOrEditCurrency = async () => {
    console.log(`Adding or Editing ${newOrEditCurrency}`);
    CurrencyStore.update((currentState) => {
      let newState = currentState;

      if (
        currentState.currency_rates
          .map((v) => v.currencyCode)
          .includes(newOrEditCurrency.currencyCode)
      ) {
        console.log("Editing");
        let current_currency_rates = [...newState.currency_rates];
        let index = current_currency_rates.findIndex(
          (v) => v.currencyCode == newOrEditCurrency.currencyCode
        );
        current_currency_rates[index].alias_name = newOrEditCurrency.alias_name;
        newState.currency_rates = [...current_currency_rates];
      } else {
        console.log("Adding");
        newState.currency_rates = [
          new CurrencyRate(
            newOrEditCurrency.currencyCode,
            newOrEditCurrency.alias_name,
            newOrEditCurrency.rate,
            newOrEditCurrency.has_manual_rate,
            newOrEditCurrency.manual_rate,
            newOrEditCurrency.adjustment
          ),

          ...newState.currency_rates,
        ];

        newState.selected_currencies = [
          newOrEditCurrency.currencyCode,
          ...newState.selected_currencies,
        ];
      }

      resetNewOrEditCurrency();

      return newState;
    });

    await sendStateToServer();
  };

  const handleChangingAdjustment = async () => {
    console.log("Handing adjustment");
    await sendStateToServer();
  };

  const resetNewOrEditCurrency = () => {
    newOrEditCurrency = {
      currencyCode: "",
      alias_name: "",
      rate: 1,
      has_manual_rate: true,
      manual_rate: 1,
      adjustment: 0,
    };
    addingNewCurrency = true;
  };

  /* const handleInput = (symbol) => { */
  /*   console.log(symbol); */
  /* }; */
  /* const handleCurrencyRateChange = (currencyRateElement) => { */
  /*   console.log(currencyRateElement); */
  /* }; */

  const handleSelectCurrency = async (selectedCurrencyName) => {
    if (selectedCurrencyName.length > 0) {
      console.log(`Selecting ${selectedCurrencyName}`);
      CurrencyStore.update((currentState) => {
        let newState = currentState;

        newState.selected_currencies = [
          selectedCurrencyName,
          ...newState.selected_currencies,
        ];

        newState.selected_currencies.sort();

        return newState;
      });

      await sendStateToServer();
      await sendStateToServer();

      selectedCurrency = "";
    }
  };

  const handleResetCurrencies = async () => {
    CurrencyStore.update((currentState) => {
      let newState = currentState;

      newState.selected_currencies = [];

      return newState;
    });

    await sendStateToServer();
  };

  $: selectedCurrencies = [];

  const updateSelectedCurrencies = (currency_model) => {
    let m_SelectedCurrencies = [];
    for (let selectedCurrency of currency_model.selected_currencies) {
      let possibleSelected = currency_model.currency_rates.filter(
        (v) => v.currencyCode === selectedCurrency
      )[0];
      if (possibleSelected) {
        m_SelectedCurrencies.push(possibleSelected);
      }
    }
    console.log("Updating selected currencies");
    selectedCurrencies = m_SelectedCurrencies;
  };

  onMount(() => {
    CurrencyStore.subscribe((currency_model) => {
      updated_current_currencies = currency_model.currency_rates;
      updateSelectedCurrencies(currency_model);
    });
  });
</script>

<Card>
  <div style="display: flex; margin-bottom: 16px;">
    <p style="margin-right: 16px;">New / Edit Currency</p>
    <input
      on:change={(e) => {
        onNewFieldChangeHandler(e);
      }}
      style="width: 56px; margin-right: 16px;"
      type="text"
      bind:value={newOrEditCurrency.currencyCode}
    />
    <input
      style="width: 96px; margin-right: 16px;"
      on:chage={() => {}}
      type="text"
      bind:value={newOrEditCurrency.alias_name}
    />
    <button
      on:click={() => {
        handleAddOrEditCurrency();
      }}>{addingNewCurrency ? "Add" : "Edit"}</button
    >
    {#if !addingNewCurrency}
      <button
        on:click={() => {
          handleDeleteCurrency();
        }}>Delete</button
      >
    {/if}
  </div>
  <div style="display: flex; margin-bottom: 16px;">
    <p style="margin-right: 16px;">Select Currency</p>
    <select
      disabled={$CurrencyStore.selected_currencies.length ===
        $CurrencyStore.currency_rates.length}
      class="add-remove-currency select-currency"
      bind:value={selectedCurrency}
      name="select-currency"
      id="select-currency"
    >
      {#each $CurrencyStore.currency_rates as currencyRate, i (currencyRate.uid)}
        {#if !$CurrencyStore.selected_currencies.includes(currencyRate.name)}
          <option value={currencyRate.currencyCode}
            >{currencyRate.currencyCode}</option
          >
        {/if}
      {/each}
    </select>
    <button
      disabled={selectedCurrency.length === 0}
      on:click={handleSelectCurrency(selectedCurrency)}>Select</button
    >
    <button
      on:click={() => {
        handleResetCurrencies();
      }}>Reset</button
    >
  </div>
  <div
    style="display: grid; 
        grid-template-columns: repeat(6, auto);
        max-width: 480px;
        "
  >
    <div class="table-cell heading-title">Row</div>
    <div class="table-cell heading-title">Manual</div>
    <div class="table-cell heading-title">Code</div>
    <div class="table-cell heading-title">Name</div>
    <div class="table-cell heading-title">Rate</div>
    <div class="table-cell heading-title">Adjustment</div>
    {#each selectedCurrencies as currencyRate, i (currencyRate.uid)}
      <div class="table-cell">
        <p>{i + 1}</p>
      </div>

      <div class="table-cell">
        <input type="checkbox" bind:checked={currencyRate.has_manual_rate} />
      </div>
      <div class="table-cell">
        <p>
          {currencyRate.currencyCode}
        </p>
      </div>
      <div class="table-cell">
        <p>
          {currencyRate.alias_name}
        </p>
      </div>
      <div class="table-cell">
        {#if currencyRate.has_manual_rate}
          <input
            on:change={handleChangingAdjustment}
            type="number"
            min="0"
            step="0.0001"
            bind:value={currencyRate.manual_rate}
          />
        {:else}
          <p>
            {currencyRate.rate}
          </p>
        {/if}
      </div>
      <div class="table-cell">
        <input
          on:change={handleChangingAdjustment}
          type="number"
          step="50"
          bind:value={currencyRate.adjustment}
        />
      </div>
    {/each}
  </div>
</Card>

<style>
  * {
    font-size: 16px;
  }

  .add-remove-currency {
    margin-right: 8px;
    width: 64px;
  }

  .table-cell {
    width: 56px;
    margin: 8px 0px;
  }

  .heading-title {
    text-align: start;
    font-size: smaller;
  }

  input[type="number"] {
    width: 72px;
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

  button {
    margin-right: 8px;
    font-size: 14px;
    color: #fff;
    border: 0;
    border-radius: 8px;
    color: #fff;
    height: 32px;
    width: 60px;
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
