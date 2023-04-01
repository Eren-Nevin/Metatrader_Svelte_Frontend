<script>
  import Calendar from "svelte-material-icons/Calendar.svelte";
  import CircularProgress from "@smui/circular-progress";
</script>

<div class="quartet" style="display: flex; flex-direction: column;">
  <div style="display: flex; justify-content: space-between;">
    <div class="blue-text">
      <Calendar color="#5ea6e5" />
      Minimum trading days
    </div>
    <div class="passed-back">
      <p class="passed-text">Passed</p>
    </div>
  </div>
  <div style="display: flex; justify-content: space-between;">
    <div style="display: flex; flex-direction: column;">
      <p class="red-text">Minimum</p>
      <p class="blue-text">Current result</p>
    </div>
    <div class="red-text" style="display: flex; flex-direction: column;">
      <p>1 Day</p>
      <p>0 Day</p>
    </div>
    <CircularProgress
      class="my-colored-circle"
      style="height: 32px; width: 32px;"
      progress="0.5"
    />
  </div>
</div>

<style>
  .my-colored-circle {
    color: #1e1f21;
  }
  .quartet {
    background-color: #1e1f21;
    margin: 16px;
    padding: 16px;
  }

  .blue-text {
    color: #5ea6e5;
  }

  .red-text {
    color: #696c7c;
  }

  .passed-back {
    color: #342629;
  }

  .passed-text {
    color: #9a2052;
  }
</style>
