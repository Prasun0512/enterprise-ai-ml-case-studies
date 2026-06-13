# Smart Consultation Recording Trigger

## Goal

Automatically start and stop consultation recording based on visual detection of
a stethoscope or similar workflow-specific object.

## Architecture Pattern

- Video frame sampling
- Object detection
- Confidence thresholding
- Temporal smoothing
- Stable on/off trigger logic
- Event logging for recording state changes

## Reliability Controls

- Minimum consecutive detection windows
- Cooldown periods between state changes
- Manual override support
- False-positive review
