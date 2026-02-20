/**
 * The properties of a car
 */
export interface ICar {
  id: number;
  user: number;
  brand: string;
  model: string;
  motor: string;
  createdAt: string;
  updatedAt: string;
}

/**
 * The properties of a User
 */
export interface IUser {
  id: number;
  is_superuser: boolean;
  username: string;
  first_name: string;
  last_name: string;
  is_staff: boolean;
  date_joined: string;
  groups: any[];
  user_permissions: any[];
}

/**
 * Generic pagination response returned by DRF.
 * Matches the custom get_paginated_response() structure.
 */
export interface PaginatedResponse<T> {
  /**
   * Total number of filtered records in the database.
   * Example: 57 cars match current filters.
   */
  count: number;

  /**
   * Total number of pages available.
   * Used to generate pagination buttons in UI.
   */
  pages: number;

  /**
   * Absolute URL of the next page.
   * Null if current page is the last one.
   */
  next: string | null;

  /**
   * Absolute URL of the previous page.
   * Null if current page is the first one.
   */
  previous: string | null;

  /**
   * Array of items for the current page.
   * This is what your UI maps over.
   */
  data: T[];

  /**
   * Current page number (1-based).
   */
  page: number;

  /**
   * Number of items per page actually used.
   * May differ if client overrides with ?page_size=...
   */
  page_size: number;
}

export interface ICarsFilterOptions {
  brands: string[];
  motors: string[];
}
