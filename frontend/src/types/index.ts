export type User = {
  id: string;
  username: string;
  full_name: string;
  profile_picture?: string;
  bio?: string;
  last_active: string;
  mutual_friends_count?: number;
  mutual_trips_count?: number;
  friend_status?: string;
};
export type Friend = {
  id: string;
  friend: User;
  created_at: string;
  mutual_trips: number;
  total_shared_expenses: string;
};
export type FriendRequest = {
  id: string;
  sender: User;
  receiver: User;
  status: string;
  created_at: string;
  updated_at: string;
};
export type TripInvitation = {
  id: string;
  trip: string;
  invited_user: User;
  invited_by: User;
  status: string;
  created_at: string;
};
export type Notification = {
  id: string;
  type: string;
  title: string;
  message: string;
  is_read: boolean;
  created_at: string;
};
export type Page<T> = {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
};
