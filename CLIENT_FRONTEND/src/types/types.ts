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
