export interface QueryCountyDetailsResponse {
  industries: Industry[];
  totals: Impacts;
}

type Impacts = {
  "economic & social/jobs/p": number;
  "economic & social/vadd/$": number;
  "impact potential/acid/kg so2-eq": number;
  "impact potential/etox/ctue": number;
  "impact potential/eutr/kg n eq": number;
  "impact potential/gcc/kg co2 eq": number;
  "impact potential/hc/ctuh": number;
  "impact potential/hnc/ctuh": number;
  "impact potential/hrsp/kg pm2.5 eq": number;
  "impact potential/htox/ctuh": number;
  "impact potential/ozon/kg cfc11-eq": number;
  "impact potential/smog/kg o3 eq": number;
  "releases/haps/kg": number;
  "releases/metl/kg": number;
  "releases/pest/kg": number;
  "resource use/enrg/mj": number;
  "resource use/land/m2*a": number;
  "resource use/mine/kg": number;
  "resource use/nren/mj": number;
  "resource use/ren/mj": number;
  "resource use/watr/m3": number;
};

export interface CountyDetails {
  county: County;
  industries: Industry[];
  totals: Impacts;
}

interface Industry {
  BEA_CODE: string;
  TOTAL_EMPLOYEES: number;
  TOTAL_ESTABLISHMENTS: number;
  TOTAL_PAYROLL: number;
  TOTAL_REVENUE: number;
  id: string;
  name: string;
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
