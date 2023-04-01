<script>
	export let progress
	const angle = 360 * progress
	
	// Adapt the logic according to the approach
	const	background = `radial-gradient(white 50%, transparent 51%),
    conic-gradient(transparent 0deg ${angle}deg, red ${angle}deg 360deg),
    conic-gradient(white 0deg, white 90deg, white 180deg, red);`;

	
	$: cssVarStyles = `--background:${background}`
</script>

<style>
#progress-circle {
  background: var(--background);
  border-radius: 50%;
  width: 80px;
  height: 80px;
	transition: all 500ms ease-in;
	will-change: transform;
}
</style>

<div id="progress-circle" style="{cssVarStyles}"></div>
