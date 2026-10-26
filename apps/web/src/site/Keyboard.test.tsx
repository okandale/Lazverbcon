import { afterEach, expect, it } from "vitest";
import { cleanup, render, screen } from "@testing-library/react";
import { Keyboard } from "./Keyboard";

afterEach(cleanup);

it.each([
  ["windows", "computer", "Typing on a computer"],
  ["mac", "computer", "Typing on a computer"],
  ["android", "phone", "Typing on a phone"],
  ["iphone", "phone", "Typing on a phone"],
  ["computer", "phone", "Typing on a phone"],
  ["phone", "computer", "Typing on a computer"],
])(
  "links from the %s instructions to the next typing guide below",
  (platform, next, title) => {
    const { container } = render(
      <Keyboard language="en" platform={platform} />,
    );
    expect(screen.queryByRole("complementary")).toBeNull();
    expect(screen.queryByText("Downloads & help")).toBeNull();
    const link = screen.getByRole("link", { name: new RegExp(title) });
    expect(link.getAttribute("href")).toBe(`/keyboard/${next}?lang=en`);
    expect(
      link.compareDocumentPosition(container.querySelector("article")!),
    ).toBe(Node.DOCUMENT_POSITION_PRECEDING);
  },
);

it.each([
  ["windows", "Keyman for Windows ↗", "https://keyman.com/windows/download"],
  ["mac", "Keyman for macOS ↗", "https://keyman.com/mac/download"],
  [
    "android",
    "Keyman on Google Play ↗",
    "https://play.google.com/store/apps/details?id=com.tavultesoft.kmapro",
  ],
  [
    "iphone",
    "Keyman on the App Store ↗",
    "https://apps.apple.com/app/keyman/id933676545",
  ],
])(
  "keeps the %s download in its installation step",
  (platform, label, href) => {
    render(<Keyboard language="en" platform={platform} />);
    const link = screen.getByRole("link", { name: label });
    expect(link.getAttribute("href")).toBe(href);
    expect(link.closest("li")).not.toBeNull();
  },
);

it("keeps Turkish on the link to the typing guide", () => {
  render(<Keyboard language="tr" platform="windows" />);
  expect(
    screen
      .getByRole("link", { name: /Bilgisayarda yazma/ })
      .getAttribute("href"),
  ).toBe("/keyboard/computer?lang=tr");
  expect(screen.queryByText("İndirme ve yardım")).toBeNull();
});
