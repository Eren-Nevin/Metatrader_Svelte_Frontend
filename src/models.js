import { v4 } from "uuid";

export class User {
  uid;
  constructor(uid) {
    this.uid = uid;
  }
}

export class TradingDays {
  min;
  current;
  passed;
  constructor(min, current, passed) {
    this.min = min;
    this.current = current;
    this.passed = passed;
  }
}

export class InitialDepositLoss {
  max_allowable;
  current;
  passed;
  constructor(max_allowable, current, passed) {
    this.max_allowable = max_allowable;
    this.current = current;
    this.passed = passed;
  }
}

export class DailyLoss {
  max_allowable;
  current;
  passed;
  constructor(max_allowable, current, passed) {
    this.max_allowable = max_allowable;
    this.current = current;
    this.passed = passed;
  }
}

export class ProfitTarget {
  target;
  current;
  passed;
  constructor(target, current, passed) {
    this.target = target;
    this.current = current;
    this.passed = passed;
  }
}

export class AppState {
  user;
  tradingDays;
  initialProfitLoss;
  dailyProfitLoss;
  profitTarget;

  constructor(
    user,
    tradingDays,
    initialProfitLoss,
    dailyProfitLoss,
    profitTarget
  ) {
    this.user = user;
    this.tradingDays = tradingDays;
    this.initialProfitLoss = initialProfitLoss;
    this.dailyProfitLoss = dailyProfitLoss;
    this.profitTarget = profitTarget;
  }
}
