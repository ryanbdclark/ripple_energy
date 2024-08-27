# Ripple Energy Custom Integration

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]

[![License][license-shield]][license]

[![hacs][hacsbadge]][hacs]
[![Project Maintenance][maintenance-shield]][user_profile]

A custom component for Ripple Energy.

## Installation

1. Use [HACS](https://hacs.xyz/docs/setup/download), and add this `https://github.com/ryanbdclark/ripple_energy` as a custom repository.
   ![image](https://github.com/user-attachments/assets/f1354cbe-36d1-4e51-8b00-3f829a83faba)
   ![image](https://github.com/user-attachments/assets/6b24882b-600f-42c1-97ac-2b5246e92e46)

2. Then in HACS search for "Ripple Energy". Select the ripple energy integration.
   ![image](https://github.com/user-attachments/assets/19d57702-270b-400e-936a-44026ddf412a)
   
4. On the Ripple Energy integration page click download in the bottom right then click download on the popup.
   ![image](https://github.com/user-attachments/assets/7e8b512f-0025-4d82-a1c5-0f07783c5a42)
   ![image](https://github.com/user-attachments/assets/a45cc5c8-ad36-4d34-9178-cd2ba5475f9b)

5. Once download is complete restart Home Assistant.
   
6. [![Add Integration][add-integration-badge]][add-integration] or in the HA UI go to "Settings" -> "Devices & Services" then click "+" and search for "Ripple Energy".
   ![image](https://github.com/user-attachments/assets/5b3b0742-d798-4afe-953c-1b93d96931c7)

7. When configuring, your [Ripple Energy API key](https://rippleenergy.com/members/settings?tab=0) is required.
   ![image](https://github.com/user-attachments/assets/e64b8340-4315-484b-bdc5-06ee65c75256)
   ![image](https://github.com/user-attachments/assets/c722b9cb-d894-44fe-8ac7-8d608dc905b1)


<!---->

## Usage

The `Ripple Energy` integration offers integration with the Ripple Energy cloud service.

This integration provides the following entities:

- Binary sensors - Generating status
- Sensors - Member capacity, member expected annual generation, average wind speed, average generator speed, average blade angle*, nacelle position, average tower base temperature, average ambient temperature, latest generated, latest earned, today generated, today earned, yesterday generated, yesterday earned, this week generated, this week earned, last week generated*, last week earned*, this month generated, this month earned, last month generated*, last month earned*, this year generated, this year earned, last year generated*, last year earned*, total generated, total earned.

Sensors marked with a * are disabled by default to use please manually enable in HA

## Options

- Seconds between polling - Number of seconds between each call for data from the Ripple Energy cloud service, default is 3600 seconds (1 hour) minimum of 10 seconds, once changed restart of HA required.

---

[commits-shield]: https://img.shields.io/github/commit-activity/w/ryanbdclark/ripple_energy?style=for-the-badge
[commits]: https://github.com/ryanbdclark/ripple_energy/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[license]: LICENSE
[license-shield]: https://img.shields.io/github/license/ryanbdclark/ripple_energy.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Ryan%20Clark%20%40ryanbdclark-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/ryanbdclark/ripple_energy.svg?style=for-the-badge
[releases]: https://github.com/ryanbdclark/ripple_energy/releases
[user_profile]: https://github.com/ryanbdclark
[add-integration]: https://my.home-assistant.io/redirect/config_flow_start?domain=ripple_energy
[add-integration-badge]: https://my.home-assistant.io/badges/config_flow_start.svg
