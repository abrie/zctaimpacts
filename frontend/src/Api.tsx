export interface QueryCountyImpactsResponse {
  industries: Industry[];
}

export interface QueryZipcodeImpactsResponse {
  industries: Industry[];
}

export const Indicators: Indicator[] = [
  {
    Code: "ACID",
    Group: "Impact Potential",
    ID: "Impact Potential/ACID/kg SO2 eq",
    Name: "Acidification Potential",
    SimpleName: "Acid Rain",
    SimpleUnit: "Kilograms Sulphur Dioxide (SO2)",
    Unit: "kg SO2 eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "CCDD",
    Group: "Waste Generated",
    ID: "Waste Generated/CCDD/kg",
    Name: "Commercial Construction and Demolition Debris",
    SimpleName: "Construction Debris",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "CMSW",
    Group: "Waste Generated",
    ID: "Waste Generated/CMSW/kg",
    Name: "Commercial Municipal Solid Waste",
    SimpleName: "Municipal Solid Waste",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "CRHW",
    Group: "Waste Generated",
    ID: "Waste Generated/CRHW/kg",
    Name: "Commercial RCRA Hazardous Waste",
    SimpleName: "Hazardous Waste",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "ENRG",
    Group: "Resource Use",
    ID: "Resource Use/ENRG/MJ",
    Name: "Energy Use",
    SimpleName: "Energy Use",
    SimpleUnit: "Megajoules (MJ)",
    Unit: "MJ",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "EUTR",
    Group: "Impact Potential",
    ID: "Impact Potential/EUTR/kg N eq",
    Name: "Eutrophication Potential",
    SimpleName: "Water Eutrophication",
    SimpleUnit: "Kilograms Nitrogen (N)",
    Unit: "kg N eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "ETOX",
    Group: "Impact Potential",
    ID: "Impact Potential/ETOX/CTUe",
    Name: "Freshwater Ecotoxicity Potential",
    SimpleName: "Freshwater Ecotoxicity",
    SimpleUnit: "Comparative Toxic Unit for Ecosystem (CTUe)",
    Unit: "CTUe",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "WATR",
    Group: "Resource Use",
    ID: "Resource Use/WATR/kg",
    Name: "Freshwater withdrawals",
    SimpleName: "Water Use",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "GHG",
    Group: "Impact Potential",
    ID: "Impact Potential/GHG/kg CO2 eq",
    Name: "Greenhouse Gases",
    SimpleName: "Greenhouse Gases",
    SimpleUnit: "Kilograms Carbon Dioxide (CO2)",
    Unit: "kg CO2 eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "HAPS",
    Group: "Chemical Releases",
    ID: "Chemical Releases/HAPS/kg",
    Name: "Hazardous Air Pollutants",
    SimpleName: "Hazardous Air Pollutants",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "HCAN",
    Group: "Impact Potential",
    ID: "Impact Potential/HCAN/CTUh",
    Name: "Human Health - Cancer",
    SimpleName: "Cancer Disease",
    SimpleUnit: "Comparative Toxic Unit for Humans (CTUh)",
    Unit: "CTUh",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "HNCN",
    Group: "Impact Potential",
    ID: "Impact Potential/HNCN/CTUh",
    Name: "Human Health - Noncancer",
    SimpleName: "Noncancer Disease",
    SimpleUnit: "Comparative Toxic Unit for Humans (CTUh)",
    Unit: "CTUh",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "HRSP",
    Group: "Impact Potential",
    ID: "Impact Potential/HRSP/kg PM2.5 eq",
    Name: "Human Health - Respiratory Effects",
    SimpleName: "Respiratory Effects",
    SimpleUnit: "Kilograms Particulate Matter",
    Unit: "kg PM2.5 eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "HTOX",
    Group: "Impact Potential",
    ID: "Impact Potential/HTOX/CTUh",
    Name: "Human Health Toxicity",
    SimpleName: "Toxic to Humans",
    SimpleUnit: "Comparative Toxic Unit for Humans (CTUh)",
    Unit: "CTUh",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "JOBS",
    Group: "Economic & Social",
    ID: "Economic & Social/JOBS/jobs",
    Name: "Jobs Supported",
    SimpleName: "Jobs Supported",
    SimpleUnit: "Employees",
    Unit: "jobs",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "LAND",
    Group: "Resource Use",
    ID: "Resource Use/LAND/m2*yr",
    Name: "Land use",
    SimpleName: "Land Use",
    SimpleUnit: "Square Meters per Year",
    Unit: "m2*yr",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "MNRL",
    Group: "Resource Use",
    ID: "Resource Use/MNRL/kg",
    Name: "Minerals and Metals Use",
    SimpleName: "Minerals and Metals Use",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "NNRG",
    Group: "Resource Use",
    ID: "Resource Use/NNRG/MJ",
    Name: "Nonrenewable Energy Use",
    SimpleName: "Nonrenewable Energy Use",
    SimpleUnit: "Megajoules (MJ)",
    Unit: "MJ",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "OZON",
    Group: "Impact Potential",
    ID: "Impact Potential/OZON/kg CFC-11 eq",
    Name: "Ozone Depletion",
    SimpleName: "Ozone Depletion",
    SimpleUnit: "Kilograms ChloroFluoroCarbon-11",
    Unit: "kg CFC-11 eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "PEST",
    Group: "Chemical Releases",
    ID: "Chemical Releases/PEST/kg",
    Name: "Pesticides",
    SimpleName: "Pesticides",
    SimpleUnit: "Kilograms",
    Unit: "kg",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "RNRG",
    Group: "Resource Use",
    ID: "Resource Use/RNRG/MJ",
    Name: "Renewable Energy Use",
    SimpleName: "Renewable Energy Use",
    SimpleUnit: "Megajoules (MJ)",
    Unit: "MJ",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "SMOG",
    Group: "Impact Potential",
    ID: "Impact Potential/SMOG/kg O3 eq",
    Name: "Smog Formation Potential",
    SimpleName: "Smog Formation",
    SimpleUnit: "Kilograms Ozone (O3)",
    Unit: "kg O3 eq",
    formatter: (n: number) => `${n}`,
  },
  {
    Code: "VADD",
    Group: "Economic & Social",
    ID: "Economic & Social/VADD/$",
    Name: "Value Added",
    SimpleName: "Value Added",
    SimpleUnit: "US Dollars ($)",
    Unit: "$",
    formatter: (n: number) => `${n}`,
  },
];

export interface Indicator {
  Code: string;
  Group: string;
  ID: string;
  Name: string;
  SimpleName: string;
  SimpleUnit: string;
  Unit: string;
  formatter: (n: number) => string;
}

export interface Industry {
  "Acidification Potential": number;
  BEA_2012_Detail_Waste_Disagg: string;
  BEA_Detail: string[];
  BEA_Sector: string;
  BEA_Summary: string;
  "Commercial Construction and Demolition Debris": number;
  "Commercial Municipal Solid Waste": number;
  "Commercial RCRA Hazardous Waste": number;
  EMP: string;
  ESTAB: string;
  "Energy Use": number;
  "Eutrophication Potential": number;
  "Freshwater Ecotoxicity Potential": number;
  "Freshwater withdrawals": number;
  "Greenhouse Gases": number;
  "Hazardous Air Pollutants": number;
  "Human Health - Cancer": number;
  "Human Health - Noncancer": number;
  "Human Health - Respiratory Effects": number;
  "Human Health Toxicity": number;
  "Jobs Supported": number;
  "Land use": number;
  "Minerals and Metals Use": number;
  NAICS: string;
  NAICS2017: string;
  "Nonrenewable Energy Use": number;
  "Ozone Depletion": number;
  Pesticides: number;
  "Renewable Energy Use": number;
  "Smog Formation Potential": number;
  "Value Added": number;
  county: string;
  state: string;
  [field: string]: number | string | string[];
}

export interface Zipcode {
  zipcode: string;
  geoid: string;
}

export interface County {
  statefp: number;
  countyfp: number;
  county_name: string;
  state_name: string;
  geoid: string;
  geometry: GeoJSON.Polygon;
}

export interface QueryCountyResponse {
  results: County[];
}

export interface QueryZipcodeResponse {
  results: Zipcode[];
}
