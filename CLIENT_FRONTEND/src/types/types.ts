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
  last_login: string;
  is_superuser: boolean;
  username: string;
  first_name: string;
  last_name: string;
  email: string;
  is_staff: boolean;
  is_active: boolean;
  date_joined: string;
  groups: any[];
  user_permissions: any[];
}
