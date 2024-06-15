# <P1-tibber-pulse-parser python service to translate P1 tibber pulse mqtt messages to homeassistant compatible mqtt messages >
# Copyright (C) 2024  Gompa

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

obisToString = {
    "1-3:0.2.8": "Version",
    "0-0:1.0.0": "Date-time-stamp",
    "0-0:96.1.1": "Equipment-identifier",
    "1-0:1.8.1": "electricity-delivered-to-client-(Tariff-1)-in-Wh",
    "1-0:1.8.2": "electricity-delivered-to-client-(Tariff-2)-in-Wh",
    "1-0:2.8.1": "electricity-delivered-by-client-(Tariff-1)-in-Wh",
    "1-0:2.8.2": "electricity-delivered-by-client-(Tariff-2)-in-Wh",
    "0-0:96.14.0": "Tariff-indicator-electricity",
    "1-0:1.7.0": "Actual-electricity-power-from-grid-in-W",
    "1-0:2.7.0": "Actual-electricity-power-to-grid-in-W",
    "0-0:96.7.21": "Number-of-power-failures-in-any-phase",
    "0-0:96.7.9": "Number-of-long-power-failures-in-any-phase",
    "1-0:99.97.0": "Power-Failure-Event-Log-(long-power-failures)",
    "1-0:32.32.0": "Number-of-voltage-sags-in-phase-L1",
    "1-0:52.32.0": "Number-of-voltage-sags-in-phase-L2",
    "1-0:72.32.0": "Number-of-voltage-sags-in-phase-L3",
    "1-0:32.36.0": "Number-of-voltage-swells-in-phase-L1",
    "1-0:52.36.0": "Number-of-voltage-swells-in-phase-L2",
    "1-0:72.36.0": "Number-of-voltage-swells-in-phase-L3",
    "0-0:96.13.0": "Text-message",
    "1-0:32.7.0": "Instantaneous-voltage-L1-in-V",
    "1-0:52.7.0": "Instantaneous-voltage-L2-in-V",
    "1-0:72.7.0": "Instantaneous-voltage-L3-in-V",
    "1-0:31.7.0": "Instantaneous-current-L1-in-A",
    "1-0:51.7.0": "Instantaneous-current-L2-in-A",
    "1-0:71.7.0": "Instantaneous-current-L3-in-A",
    "1-0:21.7.0": "Instantaneous-active-power-L1-consumption-in-W",
    "1-0:41.7.0": "Instantaneous-active-power-L2-consumption-in-W",
    "1-0:61.7.0": "Instantaneous-active-power-L3-consumption-in-W",
    "1-0:22.7.0": "Instantaneous-active-power-L1-production-in-W",
    "1-0:42.7.0": "Instantaneous-active-power-L2-production-in-W",
    "1-0:62.7.0": "Instantaneous-active-power-L3-production-in-W",
    "0-1:24.1.0": "Device-Type",
    "0-1:96.1.0": "Equipment-identifier(Gas)",
    "0-1:24.2.1": "gas-delivered-to-client-in-m3",
    "0-0:96.7.19": "powerfailure-log-entries",
}
