import { writable } from "svelte/store";
import { v4 } from "uuid";
import {
  AppState,
  TradingDays,
  InitialDepositLoss as InitialDepositLoss,
  DailyLoss,
  ProfitTarget,
  User,
} from "./models";


let app_server_address = "http://135.125.202.125:3001";

let AppStateStore = writable(null)
export async function getRawStateFromServer(uid) {
  let raw_res = await fetch(
    `${app_server_address}/api/get_goals?login=${uid}`
    // {mode: 'no-cors'}
  );

  if (!raw_res.ok) {
    console.log(raw_res.statusText);
    console.log(raw_res.status);
  }
  return await raw_res.json();
}


export async function getAppStateFromServer(uid) {
  console.log("Getting app state from server");
  let raw_state = await getRawStateFromServer(uid);

    let user = new User(uid)
    if (raw_state['success']){
        let goals = raw_state['goals']

        let tradingDaysRaw = goals['Minimum Trading Days']

        let tradingDays = new TradingDays(
            tradingDaysRaw['Minimum'],
            tradingDaysRaw['Current Result'],
            tradingDaysRaw['Reached']
        )

        let initialDepositLossRaw = goals['Initial Deposit Loss']

        let initialDepositLoss = new InitialDepositLoss(
            initialDepositLossRaw['Max Loss'],
            tradingDaysRaw['Current Result'],
            tradingDaysRaw['Reached']
        )

        let dailyLossRaw = goals['Daily Loss']

        let dailyLoss = new DailyLoss(
            dailyLossRaw['Max Loss'],
            dailyLossRaw['Current Result'],
            dailyLossRaw['Reached']
        )

        let profitTargetRaw = goals['Profit Target']

        let profitTarget = new ProfitTarget(
            profitTargetRaw['Minimum Profit'],
            profitTargetRaw['Current Result'],
            profitTargetRaw['Reached']
        )

        return new AppState(user, tradingDays,
            initialDepositLoss,  dailyLoss, profitTarget)

    }

    return null
}







async function _getAppStateFromServer() {
  console.log("Getting app state from server");
  let raw_state = await getRawStateFromServer();

  let new_dollar_model = dollarModelDataAdapter(raw_state.dollar_model);
  let new_bot_model = botModelDataAdapter(raw_state.bot_model);
  let new_currency_model = currencyModelDataAdapter(raw_state.currency_model);

  let app_state = new AppState(
    new_dollar_model,
    new_currency_model,
    new_bot_model
  );

  console.log(app_state);

  return app_state;
}

export async function reloadRatesFromServer() {
  console.log("Reloading rates from server");

  let newAppState = await _getAppStateFromServer();
  let new_currency_rates = newAppState.currency_model.currency_rates;

  CurrencyStore.update((currentState) => {
    let toBeUpdatedState = JSON.parse(JSON.stringify(currentState));
    for (let currency_rate of currentState.currency_rates) {
      if (
        new_currency_rates
          .map((e) => e.currencyCode)
          .includes(currency_rate.currencyCode)
      ) {
        let corrospondingRate = new_currency_rates.filter(
          (e) => e.currencyCode == currency_rate.currencyCode
        )[0];
        toBeUpdatedState.currency_rates.find(
          (e) => e.currencyCode == corrospondingRate.currencyCode
        ).rate = corrospondingRate.rate;
      }
    }
    return toBeUpdatedState;
  });
}

export async function reloadStateFromServer() {
  let new_app_state = await _getAppStateFromServer();
  console.log(new_app_state);

  DollarStore.update((currentState) => {
    return new_app_state.dollar_model;
  });

  BotStore.update((currentState) => {
    return new_app_state.bot_model;
  });

  CurrencyStore.update((currentState) => {
    return new_app_state.currency_model;
  });
}

let dollarUnsub;
let currencyUnsub;
let botUnsub;

export function startUpdatingAppState() {
  dollarUnsub = DollarStore.subscribe((dollar_model) => {
    app_state.dollar_model = dollar_model;
  });
  currencyUnsub = CurrencyStore.subscribe((currency_model) => {
    app_state.currency_model = {
      selected_currencies: currency_model.selected_currencies,
      currency_rates: [...currency_model.currency_rates],
    };
  });
  botUnsub = BotStore.subscribe((bot_model) => {
    app_state.bot_model = bot_model;
  });
}

export function stopUpdatingAppState() {
  dollarUnsub();
  currencyUnsub();
  botUnsub();
}

export async function sendStateToServer() {
  console.log("Sending state to server");
  let app_state_json = JSON.stringify(app_state);
  let raw_res = await fetch(`${app_server_address}/api/send_state`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: app_state_json,
  });
}
