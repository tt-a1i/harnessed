export const HarnessedPlugin = async ({ client }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.created") {
        await client.app.log({
          body: {
            service: "harnessed-opencode",
            level: "info",
            message: "Harnessed OpenCode adapter active",
          },
        })
      }
    },
    "experimental.session.compacting": async (_input, output) => {
      output.context.push("Preserve .harnessed/qa-state.md, .harnessed/contract.md, and pending human review notes across compaction.")
    },
  }
}
