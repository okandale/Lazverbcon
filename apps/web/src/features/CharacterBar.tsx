import React from "react";
import type { RefObject } from "react";

export function CharacterBar({
  value,
  onChange,
  input,
}: {
  value: string;
  onChange: (value: string) => void;
  input: RefObject<HTMLInputElement | null>;
}) {
  return (
    <div className="characters" aria-label="Laz characters">
      {["ç̌", "ǩ", "p̌", "t̆", "ǯ", "ž", "ʒ", "ş"].map((char) => (
        <button
          type="button"
          key={char}
          onClick={() => {
            const start = input.current?.selectionStart ?? value.length;
            const end = input.current?.selectionEnd ?? start;
            onChange(value.slice(0, start) + char + value.slice(end));
            input.current?.focus();
            requestAnimationFrame(() =>
              input.current?.setSelectionRange(
                start + char.length,
                start + char.length,
              ),
            );
          }}
        >
          {char}
        </button>
      ))}
    </div>
  );
}
