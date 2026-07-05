import type { ReactNode } from "react";
import {
  User,
  Friend,
  FriendRequest,
  TripInvitation,
  Notification,
} from "../types";
const Avatar = ({ u }: { u: User }) => (
  <img
    className="h-12 w-12 rounded-full object-cover"
    src={
      u.profile_picture ||
      `https://api.dicebear.com/8.x/initials/svg?seed=${u.username}`
    }
    alt={u.full_name}
  />
);
export function EmptyState({ title, body }: { title: string; body: string }) {
  return (
    <div className="glass rounded-3xl p-10 text-center">
      <h3 className="text-xl font-semibold">{title}</h3>
      <p className="text-slate-500">{body}</p>
    </div>
  );
}
export function LoadingSkeleton() {
  return (
    <div className="glass animate-pulse rounded-3xl p-5">
      <div className="h-4 w-2/3 rounded bg-slate-300" />
      <div className="mt-3 h-4 w-1/3 rounded bg-slate-300" />
    </div>
  );
}
export function ConfirmationModal({
  open,
  title,
  onConfirm,
  onCancel,
}: {
  open: boolean;
  title: string;
  onConfirm: () => void;
  onCancel: () => void;
}) {
  if (!open) return null;
  return (
    <div className="fixed inset-0 grid place-items-center bg-black/50">
      <div className="glass rounded-3xl p-6">
        <h2 className="text-lg font-bold">{title}</h2>
        <div className="mt-4 flex gap-2">
          <button className="btn bg-rose-600 text-white" onClick={onConfirm}>
            Confirm
          </button>
          <button
            className="btn bg-slate-200 dark:bg-slate-800"
            onClick={onCancel}
          >
            Cancel
          </button>
        </div>
      </div>
    </div>
  );
}
export function UserCard({ user, action }: { user: User; action?: ReactNode }) {
  return (
    <div className="glass flex items-center justify-between rounded-3xl p-4">
      <div className="flex items-center gap-4">
        <Avatar u={user} />
        <div>
          <div className="font-semibold">{user.full_name}</div>
          <div className="text-sm text-slate-500">@{user.username}</div>
          <div className="text-xs text-slate-400">
            {user.mutual_friends_count ?? 0} mutual friends •{" "}
            {user.mutual_trips_count ?? 0} mutual trips
          </div>
        </div>
      </div>
      {action}
    </div>
  );
}
export function FriendCard({
  friend,
  onInvite,
  onRemove,
}: {
  friend: Friend;
  onInvite: () => void;
  onRemove: () => void;
}) {
  return (
    <UserCard
      user={friend.friend}
      action={
        <div className="flex gap-2">
          <button className="btn bg-indigo-600 text-white" onClick={onInvite}>
            Invite to Trip
          </button>
          <button className="btn bg-rose-600 text-white" onClick={onRemove}>
            Remove
          </button>
        </div>
      }
    />
  );
}
export function FriendRequestCard({
  request,
  onAccept,
  onReject,
  onCancel,
}: {
  request: FriendRequest;
  onAccept?: () => void;
  onReject?: () => void;
  onCancel?: () => void;
}) {
  return (
    <div className="glass rounded-3xl p-4">
      <UserCard
        user={request.sender}
        action={
          <span className="rounded-full bg-amber-100 px-3 py-1 text-xs text-amber-700">
            {request.status}
          </span>
        }
      />
      <div className="mt-3 flex gap-2">
        {onAccept && (
          <button className="btn bg-emerald-600 text-white" onClick={onAccept}>
            Accept
          </button>
        )}
        {onReject && (
          <button className="btn bg-slate-700 text-white" onClick={onReject}>
            Reject
          </button>
        )}
        {onCancel && (
          <button className="btn bg-rose-600 text-white" onClick={onCancel}>
            Cancel
          </button>
        )}
      </div>
    </div>
  );
}
export function TripInvitationCard({
  invitation,
  onAccept,
  onReject,
}: {
  invitation: TripInvitation;
  onAccept: () => void;
  onReject: () => void;
}) {
  return (
    <div className="glass rounded-3xl p-5">
      <b>Trip invitation</b>
      <p>Invited by {invitation.invited_by.full_name}</p>
      <div className="mt-3 flex gap-2">
        <button className="btn bg-emerald-600 text-white" onClick={onAccept}>
          Accept
        </button>
        <button className="btn bg-slate-700 text-white" onClick={onReject}>
          Reject
        </button>
      </div>
    </div>
  );
}
export function NotificationCard({
  notification,
  onRead,
  onDelete,
}: {
  notification: Notification;
  onRead: () => void;
  onDelete: () => void;
}) {
  return (
    <div
      className={`glass rounded-3xl p-4 ${notification.is_read ? "opacity-70" : ""}`}
    >
      <h3 className="font-semibold">{notification.title}</h3>
      <p className="text-sm text-slate-500">{notification.message}</p>
      <div className="mt-2 flex gap-2">
        <button className="btn bg-indigo-600 text-white" onClick={onRead}>
          Mark read
        </button>
        <button className="btn bg-rose-600 text-white" onClick={onDelete}>
          Delete
        </button>
      </div>
    </div>
  );
}
