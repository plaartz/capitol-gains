import { createContext, useState } from "react";

export function useFilter(filterObjects = {}) {
  const [filters, setFilters] = useState(filterObjects);

  const updateFilter = (key, val) => {
    setFilters((prev) => {
      const tmp = { ...prev };
      tmp[key] = val;
      return tmp;
    });
  };

  return [filters, updateFilter];
}

export const FilterContext = createContext(() => useFilter());

export default { useFilter, FilterContext };
