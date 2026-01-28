import { useEffect, useState, useContext } from "react";
import api from "../utils/api";
import { SiteContext } from "../context/SiteContext";
import Hero from "@/components/Hero";
import Section from "../components/Section";

export default function Home() {
  const { country, branch } = useContext(SiteContext);
  const [sections, setSections] = useState([]);

  useEffect(() => {
    api.get(`/home/`).then((res) => {
      setSections(res.data.sections);
    }).catch((err) => {
      console.error("Error fetching home page:", err);
    });
  }, [country, branch]);

  // Extract hero section
  const heroSection = sections.find((sec) => sec.section_type === "hero");
  const otherSections = sections.filter((sec) => sec.section_type !== "hero");

  return (
    <div>
      <Hero data={heroSection} />
      {otherSections.map((section) => (
        <Section key={section.section_type} data={section} />
      ))}
    </div>
  );
}
