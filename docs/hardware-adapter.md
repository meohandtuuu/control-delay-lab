# Hardware adapter plan

Keep the experimental question and metrics constant while replacing the simulated plant with a motor bench.

## Minimum setup

- Low-voltage DC motor with encoder
- Motor driver with current limit
- Microcontroller or robotics board
- Emergency stop and a mechanically safe mount

## Log format

Record one CSV row per fixed-rate sample: `time_s,setpoint,position,velocity,control`. Record requested delay separately in run metadata. Use a monotonic clock and write actual timestamps rather than assuming the loop always meets its target period.

## Procedure

1. Verify encoder direction and stop behavior at low power.
2. Measure the loop period and record baseline jitter.
3. Apply the same position step at each delay setting, with repeated trials.
4. Save raw traces before calculating metrics.
5. Report the motor, encoder, driver, supply voltage, sampling rate, PID gains, and delay implementation.

The simulator is not a safety controller.

