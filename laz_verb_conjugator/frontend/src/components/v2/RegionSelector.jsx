import Chip from "@mui/material/Chip";
import { useState } from "react";

import {
    regionColors
} from "../constants";

const RegionSelector = ({initialSelectedRegions, onSelectedRegionsUpdate}) => {

  const [selectedRegions, setSelectedRegions] = useState(initialSelectedRegions);

  const regions = [
    {
        "code": "AS",
        "name": "Ardeşen",
    },
    {
        "code": "HO",
        "name": "Hopa"
    },
    {
        "code": "FA",
        "name": "Fındıklı-Arhavi"
    },
    {
        "code": "PZ",
        "name": "Pazar"
    }
  ]

  const onChipClick = (regionCode) => {
    const newSet = new Set(selectedRegions);
    if (newSet.has(regionCode)) {
        newSet.delete(regionCode);
    } else {
        newSet.add(regionCode);
    }
    setSelectedRegions(newSet);
  }

  return (
    <div className="flex gap-1">
      {regions.map((region) => (
        <Chip
          key={region["code"]}
          label={region["name"]}
          color={regionColors[region["code"]]}
          onClick={() => onChipClick(region["code"])}
           variant={selectedRegions.has(region["code"]) ? "filled" : "outlined"}
        sx={{
          opacity: selectedRegions.has(region["code"]) ? 1 : 0.2,
        }}
        />
      ))}
    </div>
  );
};

export default RegionSelector;
